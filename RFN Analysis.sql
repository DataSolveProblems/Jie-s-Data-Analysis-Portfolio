USE JJ
GO

-- SELECT TOP 100 * FROM RFM_Dataset

/** Step 1. Filter the dataset **/
WITH dataset AS (
	SELECT 
		Customer_ID,
		Order_ID,
		Order_Date,
		Sales
	FROM RFM_Dataset
	WHERE Segment = 'Consumer' AND Country = 'United States'
),

/** Step 2. Exam the dataset **/
--SELECT 
--	Customer_ID,
--	Order_ID,
--	Order_Date,
--	Sales,
--	COUNT(Order_ID) OVER(PARTITION BY Customer_ID, Order_ID)
--FROM dataset


/** Step 3. Summarize the dataset **/
Order_Summary as (
	SELECT 
		Customer_ID, Order_ID, Order_Date,
		SUM(Sales) as Total_Sales
	FROM dataset
	GROUP BY Customer_ID, Order_ID, Order_Date
)


/** Step 4. Put together the RFM Report **/
SELECT 
t1.Customer_ID,
-- (SELECT MAX(Order_Date) FROM Order_Summary) as max_order_date,
-- (SELECT MAX(Order_Date) FROM Order_Summary WHERE Customer_ID = t1.Customer_ID) as max_customer_order_date
DATEDIFF(day, (SELECT MAX(Order_Date) FROM Order_Summary WHERE Customer_ID = t1.Customer_ID), (SELECT MAX(Order_Date) FROM Order_Summary)) as Recency,
COUNT(t1.Order_ID) as Fequency,
SUM(t1.Total_Sales) as Monetary,
NTILE(3) OVER (ORDER BY DATEDIFF(day, (SELECT MAX(Order_Date) FROM Order_Summary WHERE Customer_ID = t1.Customer_ID), (SELECT MAX(Order_Date) FROM Order_Summary)) DESC) as R,
NTILE(3) OVER (ORDER BY COUNT(t1.Order_ID) ASC) F,
NTILE(3) OVER (ORDER BY SUM(t1.Total_Sales) ASC) M
FROM Order_Summary t1
GROUP BY t1.Customer_ID
ORDER BY 1, 3 DESC