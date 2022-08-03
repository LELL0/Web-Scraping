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
  
  ![image](https://user-images.githubusercontent.com/81851926/181505696-1d633b61-30bb-4aef-8f3d-22c78acc14ab.png)


### The script has a blacklist that filters the links that contains any of the keywords in there subdirectory filtering any non profile url
  (you can add or remove elements to it).
  
  ![image](https://user-images.githubusercontent.com/81851926/181505338-2ea8392b-45a3-49af-b304-f0e81c6c2482.png)


### The script Saves two files, one file with all the found links and another with the whitelisted items.

  ![image](https://user-images.githubusercontent.com/81851926/179397409-ffed665e-5e84-418e-89d4-f6f92c1324a6.png)

  - All Links:
    
    ![image](https://user-images.githubusercontent.com/81851926/182587327-9a64d468-8aad-4fb6-b1fb-ff59bdf83d25.png)


  - Whitelisted Links:
    
    ![image](https://user-images.githubusercontent.com/81851926/182587387-95c02b78-6ee0-4587-9af7-601c66006d67.png)


### Log file:

![image](https://user-images.githubusercontent.com/81851926/182587786-4b000552-69a3-454e-8eb7-067b4e79492f.png)


## Other Features:

#### not allowing redirects.
#### bypassing certificates.
#### Filtering duplicate links.
#### filter non profile links (feed, stories, stores, etc.).
#### Bypassing INCAPSULA.
#### Log file when running the script.
