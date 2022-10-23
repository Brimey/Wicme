import asyncio
from authentication import create_conn
from bs4 import BeautifulSoup
from utilities import get_response, transform_data, retrieve_keys


def main():
    client = create_conn()

    @client.event
    async def on_ready():
        url = 'https://www.gofundme.com/f/paladins-winter-cup-community-prizepool-fund/donations?member=22209235' \
              '&utm_campaign=p_cp+share-sheet&utm_medium=copy_link_all&utm_source=customer '
        curr_donators = transform_data(get_response(url))['data']
        channel = await client.fetch_channel(1029407257160597546)

        while True:
            query = get_response(url)
            donators = transform_data(query)['data']
            donation_sum = int(str(BeautifulSoup(query.text, 'lxml').find_all('p')[0]).replace(
                '<span class="text-small color-gray"> raised of $5,000 goal</span><span class="hide-for-large"> <span '
                'class="color-gray-40">•</span> </span></p>',
                '').replace('<p class="m-progress-meter-heading">', '').replace('<!-- --> ', '').replace('$',
                                                                                                         '').replace(
                ',', '')[0:5].replace('.', ''))

            for donator in donators:
                if donator not in curr_donators:
                    await channel.send(f'```{donator["name"]} donated ${donator["amount"]}.```')
            else:
                if donation_sum >= 5000:
                    await channel.send('Goal has been reached.')
                    break

            curr_donators = transform_data(query)['data']

            await asyncio.sleep(86400)

    client.run(retrieve_keys('TOKEN'))


main()
