# iCertify
You can distribute eCertificates for any good deed to massive people

![iCertify](https://github.com/piyusgupta/iCertify/blob/master/data/logo.jpg)

Product is ready for all the linux environment to use

I have tested it and written the installation manual for Ubuntu-12.04+

You need to install Pillow Image library to keep this certification ready
```
apt-get install python-dev
apt-get install libjpeg-dev
apt-get install libjpeg8-dev
apt-get install libpng3 
apt-get install libfreetype6-dev
ln -s /usr/lib/`uname -i`-linux-gnu/libfreetype.so /usr/lib
ln -s /usr/lib/`uname -i`-linux-gnu/libjpeg.so /usr/lib
ln -s /usr/lib/`uname -i`-linux-gnu/libz.so /usr/lib

pip install Pillow==3.2.0
```

App config will be created in data folder and you can edit the following content
```
[app-settings]
font-family = fonts/Verdana.ttf
font-size = 22
font-colour = (255, 255, 255)
output_format = PDF
attachments = attachments

[user-settings]
xy_cordinates = (100, 50) # This is the co-ordinates in image file from where you want to start writing name
certificate = data/certificate.jpg
send_email = True

[email-sender]
email = xxx@gmail.com
password = xyz
port = 587
pop_forwarding = smtp.gmail.com

```
The product can be used by commandline after successfull installation
>USAGE : to generate new certificate and send email
```
python certify <email_id> <full_name_with_space>
```
> ADMIN USAGE : to get the statistics for certificate generation
```
python certify --admin
```
