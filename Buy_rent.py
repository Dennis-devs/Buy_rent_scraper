from bs4 import BeautifulSoup as bs
import requests
import csv
import pandas as pd

base_url="https://www.buyrentkenya.com/houses-for-rent"
# Add user agent here
agent = ""


#input your headers here
headers = ({'User-Agent':agent, 'Accept-Language':'en-US, en;q=0.5'})
# Send a GET request to the URL
response = requests.get(base_url, headers=headers)

soup = bs(response.content, "html.parser")

# Initialize lists to store data
titles = []
locations = []
no_of_bathrooms = []
no_of_bedrooms = []
descriptions = []
prices = []
links= []

# Find all listing cards on the page
houses = soup.find_all("div", class_="listing-card" )

# Extract information from each listing
for house in houses:
    # Extract title
    title = house.find("span",class_="relative top-[2px] hidden md:inline").text.strip()
    print(title)
    # Extract location
    location = house.find("p",class_="ml-1 truncate text-sm font-normal capitalize text-grey-650").text.strip()
    # Extract number of bedrooms and bathrooms
    no_of_bedroom = house.find("span",attrs={"data-cy":"card-bedroom_count"}).text.strip()
    print(no_of_bedroom)
    no_of_bathroom = house.find("span",attrs={"data-cy":"card-bathroom_count"}).text.strip()
    # Extract description
    description = house.find("a",class_="block truncate text-grey-500 no-underline").text.strip()
    # Extract price
    price = house.find("p",class_="text-xl font-bold leading-7 text-grey-900").text.strip()
    # Extract link
    link = house.find("a",class_="text-black no-underline").get("href")

    # Append extracted data to respective lists
    titles.append(title)
    locations.append(location)
    no_of_bathrooms.append(no_of_bathroom)
    no_of_bedrooms.append(no_of_bedroom)
    descriptions.append(description)
    prices.append(price)
    links.append(link)

# Display the number of houses extracted from the first page about the first page    
print(f"The First Page No of Titles is {len(titles)}")

# Iterate through multiple pages
for page in range(2,56):
    url = f"{base_url}?page={page}"
    # Make a GET request for each page
    response = requests.get(url,headers=headers)
    print(url)
    houses = soup.find_all("div",class_="listing-card")
    for house in houses:
        # Repeat the process of extracting data from each listing
        # Extract title
        title = house.find("span",class_="relative top-[2px] hidden md:inline").text.strip()
        # Extract location
        location = house.find("p",class_="ml-1 truncate text-sm font-normal capitalize text-grey-650").text.strip()
        # Extract number of bedrooms and bathrooms
        # class_="whitespace-nowrap")[0].text.strip()
        no_of_bedroom = house.find("span",attrs={"data-cy":"card-bedroom_count"}).text.strip()
        no_of_bathroom = house.find("span",attrs={"data-cy":"card-bathroom_count"}).text.strip()
        # Extract description
        description = house.find("a",class_="block truncate text-grey-500 no-underline").text.strip()
        # Extract price
        price = house.find("p",class_="text-xl font-bold leading-7 text-grey-900").text.strip()
        # Extract link
        link = house.find("a",class_="text-black no-underline").get("href")

    # Append extracted data to respective lists
    titles.append(title)
    locations.append(location)
    no_of_bathrooms.append(no_of_bathroom)
    no_of_bedrooms.append(no_of_bedroom)
    descriptions.append(description)
    prices.append(price)
    links.append(link)
# Display the total number of titles scraped
print(f"The  Total no of Titles we have scraped is {len(titles)}") 

# Organize data into a DataFrame
# data = {
#     "Titles": titles,
#     "Locations": locations,
#     "No Of Bathrooms": no_of_bathrooms,
#     "No Of Bedrooms": no_of_bedrooms,
#     "Prices": prices,
#     "Description": descriptions
# }
data = {
    "Titles": titles,
    "Locations": locations,
    "No Of Bathrooms": no_of_bathrooms,
    "No Of Bedrooms": no_of_bedrooms,
    "Prices": prices,
    "Description": descriptions
}
df = pd.DataFrame(data)
print(df.shape)
#print(df.head(10))

# Save DataFrame to a CSV file
df.to_csv("buy_rent_kenya.csv",index=False)
