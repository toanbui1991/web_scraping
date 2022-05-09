import asyncio
import time
import pandas as pd
from arsenic import get_session, keys, browsers, services
import re

#setting


#single task
async def scraper(url, limit):
    service = services.Chromedriver(binary='./chromedriver.exe')
    browser = browsers.Chrome()
    #fix language to korean with argument '--lang=ko-KR'
    browser.capabilities = {
        "goog:chromeOptions": {"args": ["--headless", "--disable-gpu", "--no-sandbox", "--disable-dev-shm-usage", "--lang=ko-KR"]}
    }
    async with limit:
        async with get_session(service, browser) as session:
            
            await session.get(url)
            body = await session.wait_for_element(5, 'body')
            for _ in range(3):
                await body.send_keys(keys.END)
                time.sleep(5)
            num_comments = await session.wait_for_element(5, "h2#count yt-formatted-string span") #this can cause error
            num_comments = await session.get_elements('h2#count yt-formatted-string span')
            num_comments = num_comments[1]
            num_comments = int(await num_comments.get_text())
            com_per_load = 20
            num_loads = round(num_comments / com_per_load) + 1
            print('num_loads: {}'.format(num_loads))
            for _ in range(num_loads):
                await body.send_keys(keys.END)
            data = []
            title = await session.get_element('h1.title.style-scope.ytd-video-primary-info-renderer yt-formatted-string')
            title = await title.get_text()
            comments = await session.get_elements('div.style-scope.ytd-comment-renderer#body')
            # comments = [await comment.get_text() for comment in comments]
            for comment in comments:
                item = {}
                item['target_link'] = url
                item['title'] = title
                user_id = await comment.get_element('a.yt-simple-endpoint.style-scope.ytd-comment-renderer')
                item['user_id'] = await user_id.get_attribute('href')
                user_name = await comment.get_element('span.style-scope.ytd-comment-renderer')
                item['user_name'] = await user_name.get_text()
                comment_element = await comment.get_element('div.style-scope.ytd-expander#content')
                item['comment'] = await comment_element.get_text()
                data.append(item)

            data = pd.DataFrame(data)
            url_id = re.search(r'(watch\?v=)(\w+)', url).group(2)
            data.to_csv('./data/comments_{}.csv'.format(url_id))


    

#run multiple task as one
async def main(target_urls):
    limit = asyncio.Semaphore(10)

    for url in target_urls:
        
        await scraper(url, limit)

if __name__ == '__main__':
    start = time.time()
    target_urls = [
    'https://www.youtube.com/watch?v=_wlTizkaQx8',
    'https://www.youtube.com/watch?v=3WxTe01PQ3M',
    'https://www.youtube.com/watch?v=NldaLEUrIlM',
    'https://www.youtube.com/watch?v=Xm-Olrg8mfg'
    'https://www.youtube.com/watch?v=FF-vEV2F8LU',
    'https://www.youtube.com/watch?v=BCrqKq5S1as'
    'https://www.youtube.com/watch?v=f48xVaxzG2k',
    'https://www.youtube.com/watch?v=ajp9Kk4i8y0',
    'https://www.youtube.com/watch?v=BbHBYn4AGu4',
    'https://www.youtube.com/watch?v=mFZpRVl3cU0'
    ]
    asyncio.run(main(target_urls))
    end = time.time()
    period = end - start
    print('time to complete all tasks: {}'.format(period))