# Sold House Prices Case Study

This is an API to support two front-end systems for visualizing sold house prices over time and regions and it is called House Transactions API.

**House Transactions API** is created using Django and hosted on Heroku with a PostgreSQL database. 

## Data
Price Paid Data(https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads#single-file) that includes sold house transaction data for England and Wales is used in this project.

Due to the 10000 row limitation on Heroku PostgreSQL database, only 3000 rows from 2018, 2019 and 2020 data are used to populate the database

In the database each **house transaction object** has attributes:
- **id** (60 character CharField)
- **price** (Integer Field)
- **date** (YYYY-MM-DD)
- **zipcode** (10 character CharField)
- **property_type** (1 character CharField)
> There are 4 types of property available:
> **D**: Detached
> **S**: Semi-Detached
> **T**: Terraced
> **F**: Flats

There are two front-end systems to support:

- Time Series View Of Average Sold House Prices

- Histogram of Number of Transactions

## Time Series View of Average Sold House Prices(AverageHousePrices Endpoint)

For this front-end system, House Transactions API gets **Zip Code**, **From** and **To** Dates that specify time window to process.

With above parameters given, House Transactions API returns a time series analysis for that Zip Code location, returning average prices monthly for each house type available. In this case, we expect data to return average prices for each month within the given time window.

In order to make an API call to get data, a call needs to be made to the following endpoint: `https://soldhouseprices.herokuapp.com/housetransactions/averagehouseprices`

As a call without required parameters would not be valid, 3 parameters(**zip**, **from**, **to**) should be given as query parameters like the example below:
`https://soldhouseprices.herokuapp.com/housetransactions/averagehouseprices?zip=SK12&from=JUN+2018&to=AUG+2019`

In the above example we are requesting data for: 
**zip** = SK12
**from** = JUN 2018
**to** = AUG 2019

and in return we will be getting a JSON Response from the House Transactions API like the below:

```json
{
    "detached": [
        {
            "month": "2018-07-01",
            "average_price": 327500.0
        },
        {
            "month": "2019-06-01",
            "average_price": 789000.0
        }
    ],
    "semi_detached": [
        {
            "month": "2018-06-01",
            "average_price": 259000.0
        },
        {
            "month": "2019-06-01",
            "average_price": 370000.0
        }
    ],
    "terraced": [],
    "flats": [
        {
            "month": "2019-06-01",
            "average_price": 187500.0
        }
    ]
}
```

In the JSON Response, API returns for all 4 types of houses. If there are no matches for that house type, an empty list would be returned. For each house type, **month** and **average_price** information will be returned. If there is no matching data for a given month, no object will be returned for that specific month for the sake of simplicity.

## Histogram of Number of Transactions(TransactionBins Endpoint)

For this front-end system, House Transactions API gets **Zip Code** and **Date** parameters.

With above parameters given, House Transactions API returns a histogram for that Zip Code location and specified month, returning number of transactions for various price brackets regardless of house types. In this case, we expect API to return histogram frequencies for each bin and bin edges that represent ending point for each bin of the histogram. I assumed that we will have fixed bin count of 8 for this API but it is capable to work for varying bin counts with a very small modification.

In order to make an API call to get data, a call needs to be made to the following endpoint: `https://soldhouseprices.herokuapp.com/housetransactions/transactionbins`

As a call without required parameters would not be valid, 2 parameters(**zip**, **date**) should be given as query parameters like the example below:
`https://soldhouseprices.herokuapp.com/housetransactions/transactionbins?zip=DE7&date=JUN+2018`

In the above example we are requesting data for: 
**zip** = DE7
**date** = JUN 2018 (MMM YYYY Format)

and in return we will be getting a JSON Response from the House Transactions API like the below:

```json
{
	"histogram":  [
		2,
		0,
		0,
		0,
		1,
		0,
		0,
		1
	],
	"bin_edges":  [
		119950.0,
		127706.25,
		135462.5,
		143218.75,
		150975.0,
		158731.25,
		166487.5,
		174243.75,
		182000.0
	]
}
```
In the JSON Response, API returns **frequencies** for each bin of the histogram and **bin edges** that represent ending point of each histogram bin as lists. If there are no matches for a given bin, corresponding frequency would be returned as 0. 