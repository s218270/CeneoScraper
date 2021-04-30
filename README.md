## Stage 1 - extraction of all components for single opinion
1. extraction of single web page content
2. analysis of single opinion structure

|Component|CSS selector|Variable name|Data type|
|---------|------------|-------------|---------|
|Opinion|div.user-post__card|opinion||
|Opinion id|["data-entry-id"]|opinion_id||
|Author|span.user-post__author-name|author||
|Recommendation|span.user-post__author-recomendation > em|recommendation||
|Stars rating|span.user-post__score-count|stars||
|Content|div.user-post__text|content||
|Adventages|div.review-feature__col:has(> div[class$="positives"]) > div.review-feature__item|pros||
|Disadventages|div.review-feature__col:has(> div[class$="negatives"]) > div.review-feature__item|cons||
|Verification|div.review-pz|verified||
|Post date|span.user-post__published > time:nth-child(1)["datetime"]|post_date||
|Purchase date|span.user-post__published > time:nth-child(2)["datetime"]|purchase_date||
|Usefulness count|span[id^="votes-yes"]|usefulness||
|Uselessness coun|span[id^="votes-no"]|uselessness||
|Opinion|div.js_product-review|opinion|dict|
|Opinion id|["data-entry-id"]|opinion_id|str|
|Author|span.user-post__author-name|author|str|
|Recommendation|span.user-post__author-recomendation > em|recommendation|bool|
|Stars rating|span.user-post__score-count|stars|float|
|Content|div.user-post__text|content|str|
|Adventages|div.review-feature__col:has(> div[class$="positives"]) > div.review-feature__item|pros|list(str)|
|Disadventages|div.review-feature__col:has(> div[class$="negatives"]) > div.review-feature__item|cons|list(str)|
|Verification|div.review-pz|verified|bool|
|Post date|span.user-post__published > time:nth-child(1)["datetime"]|post_date|str|
|Purchase date|span.user-post__published > time:nth-child(2)["datetime"]|purchase_date|str|
|Usefulness count|span[id^="votes-yes"]|usefulness|int|
|Uselessness coun|span[id^="votes-no"]|uselessness|int|

3. extraction of single opinion components
4. transformation of extracted data to given data types
4. transformation of extracted data to given data types

## Stage 2 - extraction of all opinions from single page
1. definition of dictionary to store all components of single opinion
2. definition of list for opinions' dictionaries storing
3. implementation of loop traversing through all opinions form single page

## Stage 3 - extraction of all opinions for single product
## Stage 3 - extraction of all opinions for single product
1. implementation of loop traversing through consecutive pages with opinions
2. loading extracted opinions to .json file
3. parametrization of product id and reading product id form standard input

## Stage 4 - code refactoring
1. 