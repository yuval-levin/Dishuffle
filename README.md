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
First, create a user, via the sign-in page

<img width="477" border="1" alt="account" src="https://user-images.githubusercontent.com/57755465/95687362-d30dc280-0c0b-11eb-9ead-e4ac91ac4c8d.PNG">
<br/>
make sure to choose a valid address from the auto-complete feature.
If you don't, a warning will be presented upon pressing "Register".


#### Shuffling

<img width="481" border="1" alt="homepage_shuffle" src="https://user-images.githubusercontent.com/57755465/95687439-55968200-0c0c-11eb-965e-a00b7d62329d.PNG">
<br/>
<br/>
<img width="480"  border="1" alt="shuffled_dish" src="https://user-images.githubusercontent.com/57755465/95687518-ab6b2a00-0c0c-11eb-8814-a04f23a15245.PNG">
<br/>
The first few shuffles might be a tad slow, as user still has no cache.

#### Edit your details

<img width="478" border="1" alt="account_details" src="https://user-images.githubusercontent.com/57755465/95687579-1ae11980-0c0d-11eb-933a-705915c4b62b.PNG">
<br/> If you the update was successful, a message will appear - 


#### Recover forgotten password

<img width="538" border="1" alt="forgot_password" src="https://user-images.githubusercontent.com/57755465/95687598-4532d700-0c0d-11eb-91c0-a80473c7f593.PNG">
<br/>
Enter your email.<br/>
<img width="485" border="1" alt="forgot_passowrd_2" src="https://user-images.githubusercontent.com/57755465/95687713-fcc7e900-0c0d-11eb-892f-7ab926d507ed.PNG">
<br/>
A page with directions will follow.
<br/>
<img width="485" border="1" alt="forgot_password_3" src="https://user-images.githubusercontent.com/57755465/95687708-fa658f00-0c0d-11eb-87ec-0904c5c70394.PNG">

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