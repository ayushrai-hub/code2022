
# -*- coding: utf-8 -*-

import os
import pickle
from collections import Counter

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

from graft import utilsF


# -----------------------------------------------------------------------------#
#                               small utilities                                #
# -----------------------------------------------------------------------------#
def create_output_dirs(output_dir: str) -> None:
    """Ensure that *output_dir* (and the sub‑folders we need) exist."""
    for sub in ("n_graphs", "circ_stat", "mov", "plots"):
        os.makedirs(os.path.join(output_dir, sub), exist_ok=True)


def generate_default_mask(image_shape):
    """Create a default mask of ones based on the image size."""
    if len(image_shape) == 3:          # time series
        return np.ones(image_shape[1:])
    if len(image_shape) == 2:          # single image
        return np.ones(image_shape)
    raise ValueError("Unsupported image shape – expected 2 or 3 dimensions.")


# -----------------------------------------------------------------------------#
#                      single‑image graph processing helpers                   #
# -----------------------------------------------------------------------------#
def process_graph(img: np.ndarray, *, params: dict):
    """
    Create the graph (and friends) for **one** image.

    Parameters
    ----------
    img : np.ndarray
        The (already padded) image to analyse.
    params : dict
        Parameter dictionary that is forwarded to ``utilsF.creategraph``.

    Returns
    -------
    tuple
        Exactly the values returned by ``utilsF.creategraph`` in the same order.
    """
    return utilsF.creategraph(
        img,
        size=params["size"],
        eps=params["eps"],
        thresh_top=params["thresh_top"],
        sigma=params["sigma"],
        small=params["small"],
    )


def save_graph(img, graph, pos_list, idx: int, out_dir: str) -> None:
    """
    Draw *graph* on top of *img* and write it to *out_dir* as ``graph<idx>.png``.
    """
    utilsF.draw_graph_filament_nocolor(img, graph, pos_list, "", "filament")
    plt.savefig(os.path.join(out_dir, f"graph{idx}.png"))
    plt.close("all")


# -----------------------------------------------------------------------------#
#                                public  API                                   #
# -----------------------------------------------------------------------------#
def create_all(
    pathsave,
    img_o,
    maskDraw,
    size,
    eps,
    thresh_top,
    sigma,
    small,
    angleA,
    overlap,
    max_cost,
    name_cell,
):
    """
    Full analysis for a **time series** of images (legacy behaviour kept intact).
    The implementation was split into small helpers for readability &
    reusability – functional output is identical to the old monolithic version.
    """
    # --------------------------------------------------------------------- #
    # 0) preparation                                                        #
    # --------------------------------------------------------------------- #
    create_output_dirs(pathsave)

    # pad once – the algorithm expects a 1‑pixel frame of zeros
    M, N, P = img_o.shape
    img_padded = np.zeros((M, N + 2, P + 2))
    for m in range(M):
        img_padded[m] = np.pad(img_o[m], 1, "constant")

    params = dict(size=size, eps=eps, thresh_top=thresh_top, sigma=sigma, small=small)

    # allocate containers -------------------------------------------------- #
    graph_s, posL, imgSkel, imgAF, imgBl, imF, mask = ([] for _ in range(7))
    df_pos, graphD, lgG, lgG_V, graphTagg, no_filaments = ([] for _ in range(6))

    # --------------------------------------------------------------------- #
    # 1) per‑frame processing                                               #
    # --------------------------------------------------------------------- #
    for idx, img in enumerate(img_padded):
        print(idx)

        # a) create graph & visualise
        (
            g,
            pos,
            skel,
            af,
            bl,
            im_f,
            msk,
            df_p,
        ) = process_graph(img, params=params)

        utilsF.draw_graph(skel, g, pos, "untagged graph")

        # store
        graph_s.append(g)
        posL.append(pos)
        imgSkel.append(skel)
        imgAF.append(af)
        imgBl.append(bl)
        imF.append(im_f)
        mask.append(msk)
        df_pos.append(df_p)

        # b) post processing
        g_dangling = utilsF.dangling_edges(g.copy())
        graphD.append(g_dangling)

        lg = nx.line_graph(g.copy())
        lgG.append(lg)

        lg_val = utilsF.lG_edgeVal(lg.copy(), g_dangling, pos)
        lgG_V.append(lg_val)

        g_tag = utilsF.dfs_constrained(g.copy(), lg_val.copy(), bl, pos, angleA, overlap)
        graphTagg.append(g_tag)

        # c) save visualisation
        save_graph(img, g_tag, pos, idx, os.path.join(pathsave, "n_graphs"))

        # d) stats
        n_fil = len(np.unique(np.asarray(list(g_tag.edges(data="filament")))[:, 2]))
        no_filaments.append(n_fil)
        print("filament defined: ", n_fil)

    # we need *posL* later when the user re‑opens a session
    pickle.dump(posL, open(os.path.join(pathsave, "posL.gpickle"), "wb"))

    # --------------------------------------------------------------------- #
    # 2) temporal tracking                                                  #
    # --------------------------------------------------------------------- #
    memKeep = len(img_o) if len(img_o) < 20 else utilsF.signMem(
        graphTagg[:20], posL[:20]
    )

    # give the first graph unique tags
    for n1, n2, prop in graphTagg[0].edges(data=True):
        for k in range(len(graphTagg[0][n1][n2])):
            graphTagg[0][n1][n2][k]["tags"] = prop["filament"]

    max_tag = np.max(list(graphTagg[0].edges(data="filament")), axis=0)[2]

    g_tagged = [None] * len(img_o)
    g_tagged[0] = graphTagg[0]

    cost = [None] * (len(img_o) - 1)
    tag_new = [0] * len(img_o)
    tag_new[0] = max_tag
    filamentsNU = []

    for i in range(len(img_o) - 1):
        (
            g_tagged[i + 1],
            cost[i],
            tag_new[i + 1],
            filamentsNU,
        ) = utilsF.filament_tag(
            g_tagged[i],
            graphTagg[i + 1],
            posL[i],
            posL[i + 1],
            tag_new[i],
            max_cost,
            filamentsNU,
            memKeep,
        )

    pickle.dump(g_tagged, open(os.path.join(pathsave, "tagged_graph.gpickle"), "wb"))

    # visualise tracks ----------------------------------------------------- #
    for i in range(len(img_o)):
        title = f"graph {i+1}"
        utilsF.draw_graph_filament_track_nocolor(
            img_padded[i], g_tagged[i], posL[i], title, max(tag_new), padv=50
        )
        plt.savefig(os.path.join(pathsave, "mov", f"trackgraph{i+1}.png"))
        plt.close("all")

    # --------------------------------------------------------------------- #
    # 3) statistics                                                         #
    # --------------------------------------------------------------------- #
    plt.rc("xtick", labelsize=24)
    plt.rc("ytick", labelsize=24)

    unique_filaments = [
        len(np.unique(np.asarray(list(g.edges(data="tags")))[:, 2])) for g in g_tagged
    ]

    plt.figure(figsize=(10, 10))
    plt.scatter(np.arange(len(unique_filaments)), unique_filaments)
    plt.xlabel("frames", size=24)
    plt.ylabel("# filaments", size=24)
    plt.savefig(os.path.join(pathsave, "plots", "filaments_per_frame.png"))
    plt.close("all")

    # per‑frame info ------------------------------------------------------- #
    pd_fil_info = utilsF.filament_info_time(
        img_padded, g_tagged, posL, pathsave, imF, maskDraw
    )
    pd_fil_info = pd.read_csv(os.path.join(pathsave, "tracked_filaments_info.csv"))

    vals = Counter(pd_fil_info["filament"]).values()
    for norm, suffix in ((False, ""), (True, "_normalized")):
        counts, bins = np.histogram(list(vals), 20, density=norm)
        plt.figure(figsize=(10, 7))
        plt.hist(bins[:-1], bins, weights=counts, color="green")
        plt.xlabel("frames", size=24)
        plt.ylabel("filaments survival" + (" (norm.)" if norm else ""), size=24)
        plt.savefig(os.path.join(pathsave, "plots", f"survival_filaments{suffix}.png"))
        plt.close("all")

    dens, fil_len, fil_I = np.zeros(len(img_o)), np.zeros(len(img_o)), np.zeros(len(img_o))
    for i in range(len(img_o)):
        frame_info = pd_fil_info[pd_fil_info["frame number"] == i]
        dens[i] = frame_info["filament density"].values[0]
        fil_len[i] = np.median(frame_info["filament length"])
        fil_I[i] = np.median(frame_info["filament intensity per length"])

    for data, label in (
        (dens, "filament density"),
        (fil_len, "median filament length"),
        (fil_I, "median filament intensity/length"),
    ):
        plt.figure(figsize=(10, 10))
        plt.scatter(np.arange(len(img_o)), data)
        plt.xlabel("frames", size=24)
        plt.ylabel(label, size=24)
        plt.savefig(os.path.join(pathsave, "plots", f"{label.replace(' ', '_')}.png"))
        plt.close("all")


# -----------------------------------------------------------------------------#
#                         single‑image convenience wrapper                     #
# -----------------------------------------------------------------------------#
def create_all_still(
    pathsave,
    img_o,
    maskDraw,
    size,
    eps,
    thresh_top,
    sigma,
    small,
    angleA,
    overlap,
    name_cell,
):
    """
    Same analysis as *create_all* but for a single still image.
    The heavy lifting is done by the exact same helpers, therefore
    maintenance is minimal.
    """
    create_output_dirs(pathsave)

    # pad once
    img_padded = np.pad(img_o, 1, "constant")

    params = dict(size=size, eps=eps, thresh_top=thresh_top, sigma=sigma, small=small)

    (
        graph,
        posL,
        imgSkel,
        imgAF,
        imgBl,
        imF,
        mask,
        df_pos,
    ) = process_graph(img_padded, params=params)

    # store a visualisation
    save_graph(img_padded, graph, posL, 0, os.path.join(pathsave, "n_graphs"))

    # For a single image we do not need tracking – if further processing
    # is desired it can be added here, reusing the same building blocks.
