## WoltShuffle

### Table of Contents
- [Overview](#overview)
- [Getting Started](#getting-started)
- [Documentation](#documentation)
- [Support](#support)


### Overview
Wolt Shuffle is a Django based web-app, written in Python, meant to generate random Wolt dishes, from restauraunts near you.
In the Shuffle page you are presented with dish's image, name, price, description, and the restaurant's name in bold.

in WoltShuffle you can Shuffle , Order or 'NEVER AGAIN' - to indicate you never wish to be shuffled a certain dish.
WoltShuffle's abilities are based on:

* User database that includes users' addresses and 'NEVER AGAIN' dishes
* Cache to increase speed of shuffle 
* Wolt scraping

### Getting Started
#### How to Use Wolt Shuffle
First, create a user, via the sign-in page<br/>
<img width="551" alt="signup_marked" src="https://user-images.githubusercontent.com/57755465/95687359-d012d200-0c0b-11eb-9876-4f0583d1eab7.PNG"><br/>
You will be directed to the sign-up page 

<img width="477" border="1" alt="account" src="https://user-images.githubusercontent.com/57755465/95687362-d30dc280-0c0b-11eb-9ead-e4ac91ac4c8d.PNG">
<br/>
make sure to choose a valid address from the auto-complete feature.
If you don't, a warning will be presented upon pressing "Register".
<br/>
<img width="501" border="1" alt="register_choose_address" src="https://user-images.githubusercontent.com/57755465/95687423-3bf53a80-0c0c-11eb-9578-c4bcdc694fca.PNG">
<br/>

#### How to shuffle
<br/>
Once you've created your user, you will be redirected to the home page. <br/>
<img width="481" border="1" alt="homepage_shuffle" src="https://user-images.githubusercontent.com/57755465/95687439-55968200-0c0c-11eb-965e-a00b7d62329d.PNG">
<br/>
press SHUFFLE.
<br/>
<img width="480"  border="1" alt="shuffled_dish" src="https://user-images.githubusercontent.com/57755465/95687518-ab6b2a00-0c0c-11eb-8814-a04f23a15245.PNG">
<br/>
The first few shuffles might be a tad slow, as user still has no cache.
from any other page, click Home to reach this page.<br/>
<img width="547" border="1" alt="press_home" src="https://user-images.githubusercontent.com/57755465/95687545-dc4b5f00-0c0c-11eb-8918-f093ead7f604.PNG">

#### How to edit your details
Go to Account and edit the needed details.<br/>
<img width="478" border="1" alt="account_details" src="https://user-images.githubusercontent.com/57755465/95687579-1ae11980-0c0d-11eb-933a-705915c4b62b.PNG">
<br/> If you the update was successful, a message will appear.
<br/>
<img width="547" border="1" alt="account_updated" src="https://user-images.githubusercontent.com/57755465/95687581-1d437380-0c0d-11eb-820e-73059575f6b7.PNG">
<br/>
<br/>
#### How to recover  forgotten password
Go to the Login Page, and press forgot password. <br/>
<img width="538" border="1" alt="forgot_password" src="https://user-images.githubusercontent.com/57755465/95687598-4532d700-0c0d-11eb-91c0-a80473c7f593.PNG">
<br/>
Enter your email.<br/>
<img width="485" border="1" alt="forgot_passowrd_2" src="https://user-images.githubusercontent.com/57755465/95687713-fcc7e900-0c0d-11eb-892f-7ab926d507ed.PNG">
<br/>
A page with directions will follow.
<br/>
<img width="485" border="1" alt="forgot_password_3" src="https://user-images.githubusercontent.com/57755465/95687708-fa658f00-0c0d-11eb-87ec-0904c5c70394.PNG">
<br/>The mail you shall receive:<br/>
<img width="518" border="1" alt="password_reset_email" src="https://user-images.githubusercontent.com/57755465/95687711-fb96bc00-0c0d-11eb-875d-c86977c8d0ba.PNG">
<br/>
By clicking the link provided in the email, you will be directed to a password-reset form
<br/>
<img width="493" border="1" alt="password_reset_form" src="https://user-images.githubusercontent.com/57755465/95687712-fc2f5280-0c0d-11eb-8c25-1176edd0b96c.PNG">
<br/>

Once you have saved the new password, a success page will be presented
<br/>
<img width="489" border="1" alt="password_reset_done" src="https://user-images.githubusercontent.com/57755465/95687710-fb96bc00-0c0d-11eb-8de2-6170c958552c.PNG">

### Documentation
Consul provides several key features:

* **Wolt_scraping.py** - Includes the functions that handle Sessions, requests, and data extraction from Wolt.

* **actions.py** - Includes the main functionality of shuffle - generating dishes, filtering, and loading data from cache.

### Support
- Feel free to contact me @ yuv.levin1@gmail.com