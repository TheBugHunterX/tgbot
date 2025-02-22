import json
import aiohttp
from bot import logger

async def fetch_ai_models():
    ai_models_url = "https://gist.githubusercontent.com/bishalqx980/204d6dfa707a8d573bdbf9c2928e6296/raw/data.json"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(ai_models_url) as response:
                text_data = await response.text()
                ai_models = json.loads(text_data)
                return ai_models
    except Exception as e:
        logger.error(e)


class LLM:
    async def text_gen(prompt, only_response=True):
        """
        `only_response` returns only response text if `True`
        """
        ai_models = await fetch_ai_models()
        if not ai_models:
            return
        
        text_gen_api = ai_models["text"]
        data = {
            "prompt": prompt
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(text_gen_api, params=data) as response:
                    result = await response.json()
                    if only_response:
                        return result[0]["response"]["response"]
                    else:
                        return result
        except Exception as e:
            logger.error(e)
    

    async def imagine(prompt, file_name="imagine"):
        """
        `file_name`: file name without file extention
        """
        ai_models = await fetch_ai_models()
        if not ai_models:
            return
        
        imagine_api = ai_models["imagine"]
        data = {
            "prompt": prompt
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(imagine_api, params=data) as response:
                    result = await response.read()
                    file_path = f"downloads/{file_name}.png"
                    with open(file_path, "wb") as f:
                        f.write(result)
                    
                    return file_path
        except Exception as e:
            logger.error(e)
