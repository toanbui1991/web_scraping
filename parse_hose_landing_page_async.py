import asyncio
import time
import pandas as pd
from arsenic import get_session, keys, browsers, services
import re, os
from aiohttp import ClientTimeout

#setting


#single task
async def scraper(url, stock, limit):
    service = services.Chromedriver(binary='./chromedriver.exe')
    browser = browsers.Chrome()
    browser.capabilities = {
        "goog:chromeOptions": {"args": ["--headless", "--disable-gpu", "--no-sandbox", "--disable-dev-shm-usage", "--lang=vi-VN"]}
    }
    # browser.capabilities = {
    #     "goog:chromeOptions": {"args": ["--no-sandbox", "--disable-dev-shm-usage", "--lang=vi-VN"]}
    # }
    timeout = ClientTimeout(
        total=None, 
        connect=30,
        sock_read=30,
        sock_connect=30
    )
    async with limit:
        try:
            async with get_session(service, browser) as session:
                await session.get(url, timeout=timeout)
                body = await session.wait_for_element(5, 'body')
                for _ in range(2):
                    await body.send_keys(keys.END)
                    time.sleep(2)
                #wait for static information to appear
                await session.wait_for_element(5, "div.col-xs-12.col-sm-5.col-md-4.col-c.bg-50") #this can cause error
                #start parsing from here:
                col_one = await session.get_element('div.col-xs-12.col-sm-5.col-md-4.col-c.bg-50')
                values = await col_one.get_elements('b.pull-right')
                values = [await value.get_text() for value in values]

                col_two = await session.get_element('div.col-xs-12.col-sm-4.col-md-4.col-c-last')
                values_two = await col_two.get_elements('b.pull-right')
                values_two = [await value.get_text() for value in values_two]

                values = values + values_two
                values.append(stock)
                print('values: ')
                print(values)
                columns = ["NN mua", "% NN sở hữu", "Cổ tức TM", "T/S cổ tức", "Beta", "EPS", "P/E", "F P/E", "BVPS", "P/B", 'stock']
                data = [values] #data have to be list of list or list of dict
                data = pd.DataFrame(data, columns=columns)
                file_path = './data/hose_data_key_index.csv'
                if not os.path.exists(file_path):
                    data.to_csv(file_path, header=columns, index=False)
                else:
                    data.to_csv(file_path, mode='a', header=False, index=False)
        except Exception as e:
            print('Exception :', e)


async def scraper_all(urls, stocks, limit):

    tasks = []
    for url, stock in zip(urls, stocks):
        task = asyncio.create_task(scraper(url, stock, limit))
        tasks.append(task)
    await asyncio.gather(*tasks)


            
    

#run multiple task as one
async def main(urls, stocks, limit_number=10):
    limit = asyncio.Semaphore(limit_number)
    await scraper_all(urls, stocks, limit)

if __name__ == '__main__':

    start = time.time()
    #build target_links list
    data = pd.read_csv('./data/stocks_dict.csv')
    hose_data = data[data["Sàn"] == 'HOSE']
    print('horse_data shape: ', hose_data.shape)
    stocks = list(hose_data["Mã CK"])
    links = list(hose_data["Link"])
    batch_limit = 30
    #check if file exist delete the files
    # file_path = './data/hose_data_key_index.csv'
    # if os.path.exists(file_path):
    #     os.remove(file_path)
    # asyncio.run(main(links, stocks, batch_limit))
    end = time.time()
    period = end - start
    print('time to complete the tasks: {}'.format(period))