

import numpy as np
import matplotlib.pyplot as plt
import os
import networkx as nx
import pandas as pd
from collections import Counter
import pickle
from typing import List, Tuple, Dict, Any, Optional
from dataclasses import dataclass

from graft import utilsF

@dataclass
class ProcessingParams:
    """Parameters for graph processing."""
    size: float
    eps: float
    thresh_top: float
    sigma: float
    small: float
    angleA: float
    overlap: float
    max_cost: Optional[float] = None

@dataclass
class GraphData:
    """Container for graph processing results."""
    graph: nx.Graph
    pos_list: List
    skel_image: np.ndarray
    af_image: np.ndarray
    bl_image: np.ndarray
    im_f: np.ndarray
    mask: np.ndarray
    df_pos: pd.DataFrame
    tagged_graph: Optional[nx.Graph] = None
    num_filaments: int = 0

def create_output_dirs(output_dir: str) -> None:
    """Ensure that the specific output dir incl. subdirs exists."""
    for subdir_name in ('n_graphs', 'circ_stat', 'mov', 'plots'):
        subdir_path = os.path.join(output_dir, subdir_name)
        os.makedirs(subdir_path, exist_ok=True)

def generate_default_mask(image_shape: Tuple[int, ...]) -> np.ndarray:
    """Create a default mask of ones based on the image size."""
    if len(image_shape) == 3:  # Time-series image
        return np.ones(image_shape[1:])
    elif len(image_shape) == 2:  # Still image
        return np.ones(image_shape)
    else:
        raise ValueError("Unsupported image shape. Expected 2 or 3 dimensions.")

def process_single_image(image: np.ndarray, params: ProcessingParams, frame_idx: int = 0) -> GraphData:
    """
    Process a single image to create and tag graphs.
    
    Args:
        image: Input image (should be padded)
        params: Processing parameters
        frame_idx: Frame index for logging
        
    Returns:
        GraphData containing all processing results
    """
    print(f"Processing frame {frame_idx}")
    
    # Create initial graph
    graph, pos_list, skel_img, af_img, bl_img, im_f, mask, df_pos = utilsF.creategraph(
        image, size=params.size, eps=params.eps, thresh_top=params.thresh_top,
        sigma=params.sigma, small=params.small
    )
    
    # Draw untagged graph
    utilsF.draw_graph(skel_img, graph, pos_list, "untagged graph")
    
    # Find dangling edges and create line graph
    graph_dangling = utilsF.dangling_edges(graph.copy())
    line_graph = nx.line_graph(graph.copy())
    line_graph_valued = utilsF.lG_edgeVal(line_graph.copy(), graph_dangling, pos_list)
    
    # Run depth first search to tag filaments
    tagged_graph = utilsF.dfs_constrained(
        graph.copy(), line_graph_valued.copy(), bl_img, pos_list, 
        params.angleA, params.overlap
    )
    
    # Count filaments
    filament_edges = list(tagged_graph.edges(data='filament'))
    if filament_edges:
        num_filaments = len(np.unique(np.asarray(filament_edges)[:, 2]))
    else:
        num_filaments = 0
    
    print(f'Filaments defined: {num_filaments}')
    
    return GraphData(
        graph=graph,
        pos_list=pos_list,
        skel_image=skel_img,
        af_image=af_img,
        bl_image=bl_img,
        im_f=im_f,
        mask=mask,
        df_pos=df_pos,
        tagged_graph=tagged_graph,
        num_filaments=num_filaments
    )

def save_graph(graph_data: GraphData, image: np.ndarray, output_path: str, 
               frame_idx: int = 0, title_suffix: str = "") -> None:
    """
    Save a single graph visualization.
    
    Args:
        graph_data: GraphData containing the graph to save
        image: Original image for background
        output_path: Directory to save the graph
        frame_idx: Frame index for filename
        title_suffix: Additional title information
    """
    utilsF.draw_graph_filament_nocolor(
        image, graph_data.tagged_graph, graph_data.pos_list, 
        title_suffix, 'filament'
    )
    filename = f'graph{frame_idx}.png'
    plt.savefig(os.path.join(output_path, filename))
    plt.close('all')

def track_filaments_across_frames(graph_data_list: List[GraphData], 
                                 params: ProcessingParams) -> List[GraphData]:
    """
    Track filaments across multiple frames.
    
    Args:
        graph_data_list: List of GraphData for each frame
        params: Processing parameters
        
    Returns:
        Updated list of GraphData with tracking information
    """
    if len(graph_data_list) < 2:
        # Initialize tags for single frame
        if graph_data_list:
            for node1, node2, property in graph_data_list[0].tagged_graph.edges(data=True):
                for n in range(len(graph_data_list[0].tagged_graph[node1][node2])):
                    graph_data_list[0].tagged_graph[node1][node2][n]['tags'] = property['filament']
        return graph_data_list
    
    # Determine memory keeping strategy
    if len(graph_data_list) < 20:
        mem_keep = len(graph_data_list)
    else:
        mem_val = 20
        mem_keep = utilsF.signMem(
            [gd.tagged_graph for gd in graph_data_list[:mem_val]],
            [gd.pos_list for gd in graph_data_list[:mem_val]]
        )
    
    # Initialize first graph with unique tags
    first_graph = graph_data_list[0].tagged_graph
    for node1, node2, property in first_graph.edges(data=True):
        for n in range(len(first_graph[node1][node2])):
            first_graph[node1][node2][n]['tags'] = property['filament']
    
    # Get maximum tag from first frame
    filament_edges = list(first_graph.edges(data='filament'))
    if filament_edges:
        max_tag = np.max(np.asarray(filament_edges), axis=0)[2]
    else:
        max_tag = 0
    
    # Track filaments across frames
    tracked_graphs = [first_graph]
    current_max_tag = max_tag
    filaments_nu = []
    
    for i in range(len(graph_data_list) - 1):
        tracked_graph, cost, new_max_tag, filaments_nu = utilsF.filament_tag(
            tracked_graphs[i], graph_data_list[i + 1].tagged_graph,
            graph_data_list[i].pos_list, graph_data_list[i + 1].pos_list,
            current_max_tag, params.max_cost, filaments_nu, mem_keep
        )
        tracked_graphs.append(tracked_graph)
        current_max_tag = new_max_tag
    
    # Update graph_data_list with tracked graphs
    for i, tracked_graph in enumerate(tracked_graphs):
        graph_data_list[i].tagged_graph = tracked_graph
    
    return graph_data_list

def save_tracked_graphs(graph_data_list: List[GraphData], images: np.ndarray, 
                       output_dir: str, max_tag: int) -> None:
    """Save tracked graph visualizations."""
    for i, graph_data in enumerate(graph_data_list):
        title = f"graph {i + 1}"
        utilsF.draw_graph_filament_track_nocolor(
            images[i], graph_data.tagged_graph, graph_data.pos_list, 
            title, max_tag, padv=50
        )
        filename = f"trackgraph{i + 1}.png"
        plt.savefig(os.path.join(output_dir, "mov", filename))
        plt.close('all')

def analyze_and_plot_data(graph_data_list: List[GraphData], images: np.ndarray, 
                         output_dir: str, mask_draw: np.ndarray) -> None:
    """Perform data analysis and create plots."""
    plt.rc('xtick', labelsize=24)
    plt.rc('ytick', labelsize=24)
    
    # Count unique filaments per frame
    unique_filaments = []
    for graph_data in graph_data_list:
        edges_with_tags = list(graph_data.tagged_graph.edges(data='tags'))
        if edges_with_tags:
            unique_count = len(np.unique(np.asarray(edges_with_tags)[:, 2]))
        else:
            unique_count = 0
        unique_filaments.append(unique_count)
    
    # Plot filaments per frame
    plt.figure(figsize=(10, 10))
    plt.scatter(np.arange(len(unique_filaments)), unique_filaments)
    plt.xlabel('frames', size=24)
    plt.ylabel('# filaments', size=24)
    plt.savefig(os.path.join(output_dir, 'plots', 'filaments_per_frame.png'))
    plt.close()
    
    # Generate detailed filament information
    pd_fil_info = utilsF.filament_info_time(
        images, [gd.tagged_graph for gd in graph_data_list],
        [gd.pos_list for gd in graph_data_list], output_dir,
        [gd.im_f for gd in graph_data_list], mask_draw
    )
    
    # Load and analyze survival data
    pd_fil_info = pd.read_csv(os.path.join(output_dir, 'tracked_filaments_info.csv'))
    vals = Counter(pd_fil_info['filament']).values()
    
    # Plot survival histograms
    counts, bins = np.histogram(list(vals), 20)
    plt.figure(figsize=(10, 7))
    plt.hist(bins[:-1], bins, weights=counts, color='green')
    plt.xlabel('frames', size=24)
    plt.ylabel('filaments survival', size=24)
    plt.savefig(os.path.join(output_dir, 'plots', 'survival_filaments.png'))
    plt.close()
    
    counts, bins = np.histogram(list(vals), 20, density=True)
    plt.figure(figsize=(10, 7))
    plt.hist(bins[:-1], bins, weights=counts, color='green')
    plt.xlabel('frames', size=24)
    plt.ylabel('filaments survival', size=24)
    plt.savefig(os.path.join(output_dir, 'plots', 'survival_filaments_normalized.png'))
    plt.close()
    
    # Analyze density, length, and intensity over time
    num_frames = len(images)
    dens = np.zeros(num_frames)
    fil_len = np.zeros(num_frames)
    fil_i = np.zeros(num_frames)
    
    for i in range(num_frames):
        frame_data = pd_fil_info[pd_fil_info['frame number'] == i]
        if not frame_data.empty:
            dens[i] = frame_data['filament density'].iloc[0]
            fil_len[i] = np.median(frame_data['filament length'])
            fil_i[i] = np.median(frame_data['filament intensity per length'])
    
    # Plot filament density over time
    plt.figure(figsize=(10, 10))
    plt.scatter(np.arange(num_frames), dens)
    plt.xlabel('frames', size=24)
    plt.ylabel('filament density', size=24)
    plt.savefig(os.path.join(output_dir, 'plots', 'filament_density.png'))
    plt.close()

def create_all(pathsave: str, img_o: np.ndarray, maskDraw: np.ndarray, 
               size: float, eps: float, thresh_top: float, sigma: float, 
               small: float, angleA: float, overlap: float, max_cost: float, 
               name_cell: str) -> None:
    """
    Process time series of images for filament analysis and tracking.
    
    Args:
        pathsave: Output directory path
        img_o: Input image array (M, N, P) where M is number of frames
        maskDraw: Mask for drawing
        size, eps, thresh_top, sigma, small: Graph creation parameters
        angleA, overlap: DFS constraint parameters
        max_cost: Maximum cost for filament tracking
        name_cell: Cell name identifier
    """
    create_output_dirs(pathsave)
    
    # Pad images
    M, N, P = img_o.shape
    img_padded = np.zeros((M, N + 2, P + 2))
    for m in range(M):
        img_padded[m] = np.pad(img_o[m], 1, 'constant')
    
    # Set up parameters
    params = ProcessingParams(
        size=size, eps=eps, thresh_top=thresh_top, sigma=sigma, 
        small=small, angleA=angleA, overlap=overlap, max_cost=max_cost
    )
    
    # Process each frame
    graph_data_list = []
    for i in range(len(img_padded)):
        graph_data = process_single_image(img_padded[i], params, i)
        save_graph(graph_data, img_padded[i], 
                  os.path.join(pathsave, 'n_graphs'), i)
        graph_data_list.append(graph_data)
    
    # Save position data
    pos_lists = [gd.pos_list for gd in graph_data_list]
    pickle.dump(pos_lists, open(os.path.join(pathsave, 'posL.gpickle'), 'wb'))
    
    # Track filaments across frames
    graph_data_list = track_filaments_across_frames(graph_data_list, params)
    
    # Save tracked graphs
    tracked_graphs = [gd.tagged_graph for gd in graph_data_list]
    pickle.dump(tracked_graphs, open(os.path.join(pathsave, 'tagged_graph.gpickle'), 'wb'))
    
    # Get maximum tag for visualization
    all_tags = []
    for graph_data in graph_data_list:
        edges_with_tags = list(graph_data.tagged_graph.edges(data='tags'))
        if edges_with_tags:
            all_tags.extend([edge[2] for edge in edges_with_tags])
    max_tag = max(all_tags) if all_tags else 0
    
    # Save tracked graph visualizations
    save_tracked_graphs(graph_data_list, img_padded, pathsave, max_tag)
    
    # Perform data analysis and create plots
    analyze_and_plot_data(graph_data_list, img_padded, pathsave, maskDraw)

def create_all_still(pathsave: str, img_o: np.ndarray, maskDraw: np.ndarray,
                    size: float, eps: float, thresh_top: float, sigma: float,
                    small: float, angleA: float, overlap: float, name_cell: str) -> None:
    """
    Process a single still image for filament analysis.
    
    Args:
        pathsave: Output directory path
        img_o: Input image array (N, P) - single image
        maskDraw: Mask for drawing
        size, eps, thresh_top, sigma, small: Graph creation parameters
        angleA, overlap: DFS constraint parameters
        name_cell: Cell name identifier
    """
    create_output_dirs(pathsave)
    
    # Pad image
    img_padded = np.pad(img_o, 1, 'constant')
    
    # Set up parameters
    params = ProcessingParams(
        size=size, eps=eps, thresh_top=thresh_top, sigma=sigma,
        small=small, angleA=angleA, overlap=overlap
    )
    
    # Process the single image
    graph_data = process_single_image(img_padded, params, 0)
    
    # Save graph
    save_graph(graph_data, img_padded, os.path.join(pathsave, 'n_graphs'), 0)
    
    # Save position data
    pickle.dump([graph_data.pos_list], open(os.path.join(pathsave, 'posL.gpickle'), 'wb'))
    
    # Initialize tags for single image (no tracking needed)
    for node1, node2, property in graph_data.tagged_graph.edges(data=True):
        for n in range(len(graph_data.tagged_graph[node1][node2])):
            graph_data.tagged_graph[node1][node2][n]['tags'] = property['filament']
    
    # Save tagged graph
    pickle.dump([graph_data.tagged_graph], 
               open(os.path.join(pathsave, 'tagged_graph.gpickle'), 'wb'))
    
    # Create basic analysis for single image
    plt.rc('xtick', labelsize=24)
    plt.rc('ytick', labelsize=24)
    
    # Simple filament count plot
    plt.figure(figsize=(10, 10))
    plt.bar([0], [graph_data.num_filaments])
    plt.xlabel('Image', size=24)
    plt.ylabel('# filaments', size=24)
    plt.xticks([0], ['Still Image'])
    plt.savefig(os.path.join(pathsave, 'plots', 'filaments_count.png'))
    plt.close()
    
    print(f"Analysis complete. Found {graph_data.num_filaments} filaments.")
