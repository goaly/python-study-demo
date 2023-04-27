import dashscope

dashscope.api_key = 'NPThLfdqldcktJXQBU32ySMbvhE3h8DGEAAE0671D82B11ED8FD24A6A8A097D92'

#'Allocated quota exceeded, please increase your quota limit.'
def sample_call_streaming():
    prompt_text = '用萝卜、土豆、茄子做饭，给我个菜谱。'
    response_generator = dashscope.aigc.Generation.call(
        model='qwen-v1',
        prompt=prompt_text,
        stream=True,
        max_length=512,
        top_k=15)
    for resp in response_generator:
        print(resp.output)


sample_call_streaming()
