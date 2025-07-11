# start
from user import User
from admin import Admin
import banner
import random

# banner
banners = [banner.banner1, banner.banner2, banner.banner3]
select_banner = random.choice(banners)
select_banner()
banner.connect()