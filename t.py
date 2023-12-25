"""
This file for shell commend copy and paste just   
"""

from apps.models import Address
# from apps.address.serializer import UserAddressSerilazer
from apps.models import User, Product_item, Wishlist, Favorite, Comment, Image, Store, Chat, Product, Cart, Rate, Order, Order_type
import uuid
from django.utils.text import slugify

user = User.objects.first()
item = Product_item.objects.first()
item.to_wishlist(user)
item.to_favorites(user)

favorite = Favorite.objects.first()

item2 = Product_item.objects.last()

item2.to_favorites(user)

item.to_Wishlist.filter(user=user)
item.to_Wishlist.filter(id=user.id)
item2.favorites.add()
user2 = User.objects.get(id=6)

item2.favorites.get_or_create(user=user2)

item2.view_item.get_or_create(user=user2)

user.comment.aupdate(item=item2, comment="asdfasdfasdfasdfAbbbbbbbBBBBBBBBBBB")

i = user.comment.aupdate(
    item=item2, comment="asdfasdfasdfasdfAbbbbbbbBBBBBBBBBBB")

#  dir(user.comment.aupdate(item=item2,comment="asdfasdfasdfasdfAbbbbbbbBBBBBBBBBBB"))

item.rate.create(user=user2, rating=5)

item.to_rate(user=user, rate=5)

u = User.objects.get(id=6)

u.image.delete()

im = Image.objects.first()

im.image.name

im.image.name = 'Products_image./Screenshot_from_2023-02-22_01-46-36_RnX3Ix.png'
im.save()

s = Store.objects.first()

user = User.objects.first()
user.follow.get_or_create(store_id=s.id)
user.add_follow(2)
a = user.add_follow(3)
bool(user.add_follow(1))

bool(user.add_follow(2))

user.chat_sender.all()

user.chat_reciever.all()

user.chat_sender.create(reciever_id=6, message="asdfasdfasdf")

b = user2.chat_reciever.get(id=8)

b = user.chat_sender.get(id=8)

b.status = True

b.save()


user = User.objects.first()
user2 = User.objects.get(id=6)

b = user2.chat_reciever.filter(sender_id=1)

user2.chat_reciever.filter(sender_id=1, status=False)

user2.chat_reciever.filter(sender_id=1, status=False).exists()
list = user2.chat_reciever.filter(sender_id=1, status=False)
user2.set_list_messages_as_red()

list = [{'id': 26, }, {'id': 27, }, {'id': 28, }, {
    'id': 29, }, {'id': 30, }, {'id': 24, }, {'id': 25, }]

list = [{'id': 19, }, {'id': 20, }, {'id': 22, }, {
    'id': 21, }, {'id': 23, }, {'id': 24, }, {'id': 25, }]

user2.set_list_messages_as_red(list)

u = User.objects.get(id=11)

u.is_deleted = False
u.save()
address = Address.objects.first()

inc = Product.objects.get(id=408)

u = Product.objects.update(product_image=inc.product_image)


s = item.item_Cart.get(user_id=13, count=20)
s.count = 304
s.count = 304
count = Product_item.objects.get(id=6)
count.item_Cart.get(user_id=1)
count.item_Cart.get(user_id=1).count

s = user.user_cart.first()
s = user.user_cart.first().id
p = Product_item.objects.first()
p.item_Cart.get(user_id=1, item_id=p.id)

Product.objects.create(category_id=1, product_name="asdfasdf",
                       product_description="asfasdf", store_id=1)
Product.objects.all().update(
    sulg=f"-{str(uuid.uuid4())[:8]}")
inc = Product.objects.last()

item = Product_item.objects.all().update(
    sulg=f"-{slugify(str(uuid.uuid4())[:8])}")


Store.objects.all().update(sulg=f"-{slugify(str(uuid.uuid4())[:15])}")

s = Store.objects.filter(sulg='-5b0b8abf')
