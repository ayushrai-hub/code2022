import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from mpl_toolkits.mplot3d import Axes3D
import time

class Manipulator6DOF:
    def __init__(self, root):
        self.root = root
        self.root.title("6-DOF Manipulator Simulation")
        
        # Manipulator parameters (link lengths in meters)
        self.links = [0.1, 0.3, 0.25, 0.2, 0.15, 0.1]
        self.joint_angles = np.zeros(6)  # Initial joint angles in radians
        
        # Setup GUI
        self.setup_gui()
        
        # Setup plot
        self.fig = plt.Figure(figsize=(8, 6))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
        
        # Initial plot
        self.update_plot()

    def setup_gui(self):
        # Control frame
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Coordinate inputs
        tk.Label(control_frame, text="Target X:").pack()
        self.x_entry = tk.Entry(control_frame)
        self.x_entry.pack()
        
        tk.Label(control_frame, text="Target Y:").pack()
        self.y_entry = tk.Entry(control_frame)
        self.y_entry.pack()
        
        tk.Label(control_frame, text="Target Z:").pack()
        self.z_entry = tk.Entry(control_frame)
        self.z_entry.pack()
        
        # Move button
        tk.Button(control_frame, text="Move to Target", command=self.move_to_target).pack(pady=10)
        
        # Reset button
        tk.Button(control_frame, text="Reset", command=self.reset).pack()

    def forward_kinematics(self, angles):
        """Calculate forward kinematics for 6-DOF manipulator"""
        positions = [np.array([0, 0, 0])]
        T = np.eye(4)
        
        for i, (angle, length) in enumerate(zip(angles, self.links)):
            # Simple DH parameters approximation
            R = np.array([
                [np.cos(angle), -np.sin(angle), 0],
                [np.sin(angle), np.cos(angle), 0],
                [0, 0, 1]
            ])
            t = np.array([0, 0, length])
            
            if i >= 3:  # Wrist adjustments
                R = np.array([
                    [1, 0, 0],
                    [0, np.cos(angle), -np.sin(angle)],
                    [0, np.sin(angle), np.cos(angle)]
                ])
            
            T_new = np.eye(4)
            T_new[:3, :3] = R
            T_new[:3, 3] = t
            T = T @ T_new
            positions.append(T[:3, 3])
        
        return np.array(positions)

    def inverse_kinematics(self, target):
        """Simplified IK solver using numerical optimization"""
        def error(angles):
            pos = self.forward_kinematics(angles)[-1]
            return np.sum((pos - target) ** 2)
        
        # Simple gradient descent
        angles = self.joint_angles.copy()
        learning_rate = 0.01
        for _ in range(100):
            grad = np.zeros(6)
            eps = 0.0001
            for i in range(6):
                angles_plus = angles.copy()
                angles_plus[i] += eps
                grad[i] = (error(angles_plus) - error(angles)) / eps
            
            angles -= learning_rate * grad
            
            if error(angles) < 0.001:  # Convergence threshold
                break
                
        return angles

    def update_plot(self):
        """Update the 3D visualization"""
        self.ax.clear()
        
        # Calculate current position
        positions = self.forward_kinematics(self.joint_angles)
        
        # Plot manipulator
        self.ax.plot(positions[:, 0], positions[:, 1], positions[:, 2], 
                    'bo-', linewidth=2, markersize=8)
        
        # Plot base and end-effector specifically
        self.ax.scatter([0], [0], [0], c='r', s=100)  # Base
        self.ax.scatter([positions[-1, 0]], [positions[-1, 1]], [positions[-1, 2]], 
                       c='g', s=100)  # End-effector
        
        # Set limits
        self.ax.set_xlim(-0.5, 0.5)
        self.ax.set_ylim(-0.5, 0.5)
        self.ax.set_zlim(0, 1)
        
        # Labels
        self.ax.set_xlabel('X (m)')
        self.ax.set_ylabel('Y (m)')
        self.ax.set_zlabel('Z (m)')
        self.ax.set_title('6-DOF Manipulator')
        
        self.canvas.draw()

    def move_to_target(self):
        """Animate movement to target position"""
        try:
            target = np.array([
                float(self.x_entry.get()),
                float(self.y_entry.get()),
                float(self.z_entry.get())
            ])
            
            # Calculate target angles
            target_angles = self.inverse_kinematics(target)
            
            # Animation steps
            steps = 20
            angle_steps = (target_angles - self.joint_angles) / steps
            
            for _ in range(steps):
                self.joint_angles += angle_steps
                self.update_plot()
                self.root.update()
                time.sleep(0.05)  # Animation speed
            
            self.joint_angles = target_angles
            self.update_plot()
            
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter valid numerical coordinates")

    def reset(self):
        """Reset manipulator to initial position"""
        self.joint_angles = np.zeros(6)
        self.x_entry.delete(0, tk.END)
        self.y_entry.delete(0, tk.END)
        self.z_entry.delete(0, tk.END)
        self.update_plot()

def main():
    root = tk.Tk()
    app = Manipulator6DOF(root)
    root.mainloop()

if __name__ == "__main__":
    main()
