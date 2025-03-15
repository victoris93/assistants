## Local AI Assistants to The People

How to implement LLMs locally as quick actions using `llama-index` (on Mac).

### Pre-requisites

- Istall [Ollama](https://ollama.com/download)
- Create a conda environment using `reqiuirements.txt` like so: 

```shell
conda create -n env_name python=3.12
conda activate env_name
pip install -r requirements.txt
```

### 2. Create a quick action in using Automator on Mac

#### 2.1. Open Automator and pick "Quick Action"

The quick action you configure will show in any application where text input is possible (text editor, browser, etc.)

![image](guide_steps_screens/open_automator_pick_quick_action.png)

#### 2.2. Create a shell command which will call the Python script

Search `Run Shell Script` in the Library using the search tool and drag and drop this option in your quick action.

![image](guide_steps_screens/search_shell_script.png)

#### 2.3. Configure the shell command

The command should call the Python script using the Python executable in the `conda` environment you had configured earlier. The script takes two arguments: 
- `model`: the name of the model fetched by `llama_index`. This is only limited by your hardware.
- `input`: text input the model takes (not the same as prompt). In the case of `render_latex_eq.py`, the input is Python code performing maths operations.
![image](guide_steps_screens/automator_shell_command.png)

#### 2.4. Save the quick action

![image](guide_steps_screens/save_quick_action.png)
![image](guide_steps_screens/name_quick_action.png)

### 3. Profit

Here's an example of how you can render $\LaTeX\$ formula from your code directly in Overleaf:

![image](demos/demo_formula_rendering.gif)


