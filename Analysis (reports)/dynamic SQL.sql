DECLARE @SQL NVARCHAR(155)

SET @SQL = 'SELECT TOP 10 * FROM CMRCUSTOMER';
EXEC SP_EXECUTESQL @SQL

-- Alternative --
DECLARE @TableName as varchar(100)

SET @TableName = 'CMRCustomerComplianceInformation'

EXEC ('SELECT TOP 10 * FROM ' + @TableName)

-------------------------------------------------------------------------------------------------
-- Alternative
DECLARE @sqlCommand nvarchar(1000)
DECLARE @columnList varchar(75)
DECLARE @city varchar(75)
SET @columnList = 'CustomerID, ContactName, City'
SET @city = 'London'
SET @sqlCommand = 'SELECT ' + @columnList + ' FROM customers WHERE City = @city'
EXECUTE sp_executesql @sqlCommand, N'@city nvarchar(75)', @city = @city
