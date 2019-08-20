from uplink import Consumer, Body, get, headers, returns


@headers({
    "User-Agent": "Uplink-Sample-App"
})
class Kraken(Consumer):

    @returns.json
    @get("0/public/Time")
    def get_time(self):
        """return the time"""


k = Kraken(base_url="https://api.kraken.com/")

print(k.get_time())

