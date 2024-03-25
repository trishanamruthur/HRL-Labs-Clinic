import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
import os

UMAX = 10
YMIN = -2
YMAX = 4
NUM = 100
tc = 0.1

script_dir = os.path.dirname(__file__)
results_dir = os.path.join(script_dir, 'Results/')

if not os.path.isdir(results_dir):
    os.makedirs(results_dir)

def get_evals(epsilon, tc=0.1, U=UMAX):
    H = np.array([[U-epsilon, math.sqrt(2)*tc, 0], [math.sqrt(2)*tc, 0, math.sqrt(2)*tc], [0, math.sqrt(2)*tc, U+epsilon]])
    evals = np.linalg.eigvalsh(H)
    return evals

def create_video(tc_values):
    frames = []

    for tc in tc_values:
        fig, ax = plt.subplots()
        get_evals_plot(tc=tc)
        ax.axis('on')  # Turn off axis to avoid unnecessary white space

        # Add title and text annotation
        plt.title(f'Spaghetti Diagram\nValue of U: {UMAX}\n t_c = {tc:.2f}', fontsize=12)
        
        plt.xlabel("Detuning")
        plt.ylabel("Energy")

        # Create a canvas and render the figure
        canvas = FigureCanvas(fig)
        canvas.draw()

        # Convert the figure to an array
        frame = np.array(canvas.renderer.buffer_rgba())
        frames.append(frame)
        plt.close(fig)  # Close the figure to free up resources

    # Create a video from the frames
    video_file = os.path.join(script_dir, "tc_spag_3.mp4")
    clip = ImageSequenceClip(frames, fps=100)
    clip.write_videofile(video_file, codec='libx264', audio=False)

def get_evals_plot(tc=0.1, U=UMAX):
    biases = np.linspace(-2 * UMAX, 2 * UMAX, NUM)

    e1 = np.zeros(NUM)
    e2 = np.zeros(NUM)
    e3 = np.zeros(NUM)

    for i in range(NUM):
        evals = get_evals(epsilon=biases[i], tc=tc, U=U)
        evals = sorted(evals)
        e1[i] = evals[0]
        e2[i] = evals[1]
        e3[i] = evals[2]

    plt.plot(biases, e1, label='Eigenvalue 1')
    plt.plot(biases, e2, label='Eigenvalue 2')
    plt.plot(biases, e3, label='Eigenvalue 3')

    # Add legend
    plt.legend()

# Define the range of tc values you want to visualize
tc_values_to_visualize = np.linspace(0.05, 5, 1000)

# Create the video
create_video(tc_values_to_visualize)