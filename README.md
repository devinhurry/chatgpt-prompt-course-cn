# About
把吴恩达prompt课程的notebook翻译成中文 for https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/.

- 大部分翻译是由chatgpt 完成的，把prompt也翻译成了中文，可以参考这个python脚本。但是翻译的prompt做的也不是特别好，翻译代码的时候有时会出现意想不到的结果，所以手动调整了一部分。
- 实践过程中会发现中文prompt的效果没有英文好，有少部分例子英文是成功的但是中文失败了。
- 这个课程还是比较浅显的，对照我这个中文notebook，半个小时就看完了。
# Setup

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

create a `.env` file and include your OpenAI API key:

```
OPENAI_API_KEY=sk-xxxx
```

Then, run the notebooks using VSCode. 


