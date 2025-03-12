import click
import sys
from llama_index.llms.ollama import Ollama


@click.command()
@click.argument("model", type=str)
@click.argument("input", type=str, required=False)
def fix_language(model, input):
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
            f"Check style and grammar in this text. Rewrite if necessary maintaining the overall length and tone."
            f"(if it's formal. keep it formal; if it's informal, also keep it that way. Do not in any way change the tone)."
            f"Explain the changes."
            f"The text is:\n{text}"
            "[/INST]"
        )
    
    llm = Ollama(model=model)
    result = llm.complete(command)
    click.echo(f"Using {model}: \n" + "*" * 25 + "\n" + str(result))

    return 0

if __name__ == "__main__":
    fix_language()
