 WEEK_START = 1 means weeks starting from 1 on Monday(keeping the default 0 means weeks starting form 0 on Sunday)
alter session set WEEK_START  = 1;

create or replace table analytics_prod.dwh.dim_date as
(
with dates as(
select date from(
select
  dateadd(day, '-' || seq4(), current_date()) as date
from
  table
    (generator(rowcount => 50000))
    
union all
 select
  dateadd(day,seq4() + 1, current_date()) as date
from
  table
    (generator(rowcount => 50000)) 
    ) dts
    where date between '1900-1-1' and '2099-12-31'
)

select 
date,
dayofweek(date)  as day_of_week,
dayofmonth(date) day_of_month,
dayofyear(date) as day_of_year,
date_trunc('week',date) as  start_of_week_date,
LAST_DAY(date,'week') as  end_of_week_date,
--Changing abbrevations to full day names
decode(DAYNAME(date), 'Mon','Monday', 'Tue','Tuesday', 'Wed','Wednesday','Thu','Thursday','Fri','Friday','Sat','Saturday','Sun','Sunday') as day_of_week_name,
 date_part(week,date) as Week_number,
  date_part(month,date) as Month_number,
 decode(monthname(date), 'Jan','January', 'Feb','February', 'Mar','March','Apr','April','May','May','Jun','June','Jul','July','Aug','August','Sep','September','Oct','October','Nov','November','Dec','December') as Month_name,
   date_trunc(month,date) as Month_in_Year,
  date_part(Quarter,date) as Quarte_number,
  date_trunc(Quarter,date) as Quarter_in_year,
  date_part(year,date) as year,
  CASE WHEN dayofweek(date) in (6,7) then true else false end as Weekend_ind,
  CASE WHEN date =  LAST_DAY(date,'month') then true else false end as last_day_in_month_ind
from dates 

)