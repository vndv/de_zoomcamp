SELECT count(*) 
  FROM green_trip_data gtd;


SELECT count(*) 
  FROM zone_lookup zl; 


-- Count records 
SELECT count(*)
  FROM green_trip_data gtd 
 WHERE CAST(lpep_pickup_datetime AS DATE) = '2019-01-15'
   AND CAST(lpep_dropoff_datetime  AS DATE)  = '2019-01-15';
   
-- Largest trip for each day
SELECT CAST(lpep_pickup_datetime AS DATE) AS pickup,
       MAX(trip_distance)
  FROM green_trip_data gtd 
 GROUP BY CAST(lpep_pickup_datetime AS DATE)
 ORDER BY 2 DESC;
 
-- The number of passengers
SELECT count(*) AS count_of_passangers,
       '2' AS number_of_passangers
  FROM green_trip_data gtd 
 WHERE CAST(lpep_pickup_datetime AS DATE) = '2019-01-01'
   AND passenger_count = 2
 UNION
SELECT count(*) AS count_of_passangers,
       '3' AS number_of_passangers
  FROM green_trip_data gtd 
 WHERE CAST(lpep_pickup_datetime AS DATE) = '2019-01-01'
   AND passenger_count = 3;
   

-- Largest tip
SELECT zl."Zone" as zone_name,
       max(gtd.tip_amount) as largest_tip 
  FROM green_trip_data gtd 
  JOIN zone_lookup zl 
    ON gtd."DOLocationID"  = zl."LocationID" 
 WHERE gtd."PULocationID" IN 
                             (
                               SELECT zl2."LocationID" 
                                 FROM zone_lookup zl2 
                                WHERE zl2."Zone" LIKE 'Astoria%'
                             )
 GROUP BY zl."Zone" 
 ORDER BY 2 desc
 LIMIT 1;


