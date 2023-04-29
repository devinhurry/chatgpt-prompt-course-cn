import openai
import os
import json
from tqdm import tqdm
from dotenv import load_dotenv, find_dotenv
import sys
_ = load_dotenv(find_dotenv())

openai.api_key  = os.getenv('OPENAI_API_KEY')

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def translate_text(text):
    example_text = """
# Setup
The following cell read the OpenAI API Key from `.env` file:
```
import openai
mykey = "Hello, World"
```    
    """
    markdown_prompt = f"""
translate text delimited by <block></block> to Chinese. 

Example:
text:
<block>
Hello,
World.
```python
a = "Hello, World"
```
</block>
Translation:
你好，
世界。
```python
a = "Hello, World"
```

Text:
<block>
{text}
</block>
Translation:
"""
    return get_completion(markdown_prompt)


def translate_code(code):
    if code == "":
        return ""
    example_code = """
text = f\"\"\"
You should express what you want a model to do by \ 
providing instructions that are as clear and \ 
specific as you can possibly make them. \ 
This will guide the model towards the desired output, \ 
and reduce the chances of receiving irrelevant \ 
or incorrect responses. Don't confuse writing a \ 
clear prompt with writing a short prompt. \ 
In many cases, longer prompts provide more clarity \ 
and context for the model, which can lead to \ 
more detailed and relevant outputs.
\"\"\"
prompt = f\"\"\"
Summarize the text delimited by triple backticks \ 
into a single sentence.
```{text}```
\"\"\"
response = get_completion(prompt)
print(response)
"""
# You should preserve the new line character and back slash same as the original code and string.\
    sep = "Step2Seperator======"
    prompt = f"""
Translate string in python code delimited by <block></block> to Chinese.
You are doing it as following steps.
Step 1. Do the translation.
Step 2. seperate the long string using backslash and new line


Example:
text:
<block>
text1 = "hello, world"
text2 = "Oh my god, this is a part of very long paragraph,\
which you should separate using backslash
"
</block>

Step 1:
text1 = "你好，世界"
tex2 = "哦，我的天啊，这是一个非常长的段落的一部分，你应该使用反斜杠来分隔它。"

Step 2:
{sep}
text1 = "你好，世界"
tex2 = "哦，我的天啊，这是一个非常长的段落的一部分，\\\n你应该使用反斜杠来分隔它。"


Text:
<block>
{code}
</block>
Step 1:
"""

    res = get_completion(prompt)
    pos = res.find(sep)
    return res[pos + len(sep) + 1:]

#If there is code delimited triple backtick, You should not translate that code

# print(translate_code(""))
# print(translate(""))


def translate_notebook(notebook_path):
    with open(notebook_path, "r", encoding="utf-8") as f:
        notebook = json.load(f)

    for i, cell in tqdm(enumerate(notebook["cells"]), desc=f"Translating {notebook_path}"):
        if cell["cell_type"] == "markdown":
            cell["source"] = [translate_text(''.join(cell["source"]))]
        elif cell["cell_type"] == "code":
            cell["source"] = [translate_code(''.join(cell["source"]))]


    new_notebook_path = os.path.splitext(notebook_path)[0] + "_cn.ipynb"
    with open(new_notebook_path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, ensure_ascii=False)

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        filename = sys.argv[1]
        translate_notebook(filename)
    else:
        for file in sorted(os.listdir(".")):
            if file.endswith("_cn.ipynb"):    
                continue
            if file.endswith(".ipynb"):
                if os.path.exists(file.replace(".ipynb", "_cn.ipynb")):
                    continue
                translate_notebook(file)

