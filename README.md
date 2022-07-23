# Web-Scraping
 It's a web scraping tool, that harvests social media links.

## Input:

- The input can be done in the command line or after you run the script:
  - at runtime:
  
    ![image](https://user-images.githubusercontent.com/81851926/179396781-fa4efa6c-0db0-4a57-b198-40a3c6f6a173.png)
    
  - in the command line:
  
    ![image](https://user-images.githubusercontent.com/81851926/179396906-358e066f-fc19-4e75-91de-e6623e78c14f.png)


- The input can be of three types:

  - URL (contains HTTP:// or HTTPS:// or www. or combination between them).
    - it will try to scrap it directly
    
      ![image](https://user-images.githubusercontent.com/81851926/179396964-c4e40e27-0a52-4795-aef3-5c7f5f0c4a68.png)

  - domain (ex: megacorpone.com).
    - will try to scrap it as it is first then try all the different combinations until it finds a valid one.
     
     ![image](https://user-images.githubusercontent.com/81851926/179397177-9bc5f010-c537-484a-8b17-04035efba72c.png)

  - Ip (ex: 127.0.0.1).
    - will try to scrape it as it is then try to add HTTP and then HTTPS to change the port.
      
      ![image](https://user-images.githubusercontent.com/81851926/179397522-0c17d6e3-8ae6-4baa-898d-c97765120804.png)


### The script checks if the website is valid.
  
  ![image](https://user-images.githubusercontent.com/81851926/179397242-5b11cfa0-4c68-4977-8f02-a7189d3e2bd8.png)

### The script checks for captcha.
  
  ![image](https://user-images.githubusercontent.com/81851926/179397219-c3b14460-4895-438f-87a4-80224acabdf8.png)

### The script has a whiteList that filters the links that we are interested in (you can add or remove elements to it).
  
  ![image](https://user-images.githubusercontent.com/81851926/179397367-66af6c25-e350-4fe3-a80e-fcf191feedc1.png)

### The script Saves two files, one file with all the found links and another with the whitelisted items.

![image](https://user-images.githubusercontent.com/81851926/179397409-ffed665e-5e84-418e-89d4-f6f92c1324a6.png)

  - All Links:
    
    ![image](https://user-images.githubusercontent.com/81851926/179397440-a31f90d8-d875-490e-9ba0-f95a61e9f81b.png)

  - Whitelisted Links:
    
    ![image](https://user-images.githubusercontent.com/81851926/179397458-554923df-c156-4b79-9beb-9a774faa47b4.png)

## Other Features:

#### not allowing redirects.
#### bypassing certificates

