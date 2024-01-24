import PySimpleGUI as sg
import matplotlib.pyplot as plt
from io import BytesIO


def render_latex_to_image(latex_formula, dpi=100):
    fig, ax = plt.subplots(figsize=(2, 2), dpi=dpi)
    ax.text(0.5, 0.5, f"${latex_formula}$", size=20, ha='center', va='center')
    ax.axis('off')

    image_stream = BytesIO()
    fig.savefig(image_stream, format='png', bbox_inches='tight', pad_inches=0, transparent=True)
    image_stream.seek(0)

    return sg.Image(data=image_stream.getvalue(), background_color='white', key='image')


def main():
    latex_formula = r'\frac{1}{2} \cdot \pi \cdot r^2'  # Example LaTeX formula for the area of a circle

    layout = [
        [sg.Frame('LaTeX Formula Display', [[render_latex_to_image(latex_formula)]])],
        [sg.Button('Exit')]
    ]

    window = sg.Window('LaTeX Formula in PySimpleGUI', layout, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break

    window.close()


if __name__ == "__main__":
    main()
