import click
import sys
from llama_index.llms.ollama import Ollama

@click.command()
@click.argument("model", type=str)
@click.argument("input", type=str, required=False)
def render_eq(model, input):
    if input is None:
        text = sys.stdin.read()
    else:
        try:
            with open(input, 'rb') as file:
                text = file.read().decode('utf-8')
        except FileNotFoundError:
            text = input

    command = (
            "[INST]"
            f"Parse the code you are given and identify mathematical operations within."
            f"Output a mathematical formula in LaTeX reflecting these operations."
            "The formula itself should start with "
            "\begin{equation} and end with \end{equation}."
            f"Explain how you came up with this formula step-by-step."
            f"Be brief. Only output what I asked. DOn't ovesimplify the formulas (e.g., mean is the sum of all elements divided by the number thereof)."
            f"If there are fractions, make sure that the branckets have the same height as the fraction."
            f"The code is:\n{text}"
            "[/INST]"
        )
    
    llm = Ollama(model)
    result = llm.complete(command)
    click.echo(f"{text}\n\n" + str(result))

    return 0

if __name__ == "__main__":
    render_eq()
