use covid;

select * from coviddeaths;

select * from covidvaccinations;

desc coviddeaths;
desc covidvaccinations;

select * from coviddeaths order by date;

alter table coviddeaths modify column date date; 

#modify column name date to date_text


#To add a column called dates 
Alter table coviddeaths add column dates date; 
#Update table dates with values of date column
Update coviddeaths set dates=str_to_date(date,'%m/%d/%y');

#now drop date column
alter table coviddeaths drop column date;

#rename column dates to date
alter table coviddeaths rename column dates to date;

select * from coviddeaths order by date;
# do the same to covidvaccination table
select * from coviddeaths;

alter table covidvaccinations add column dates date;

update covidvaccinations set dates=str_to_date(date,'%m/%d/%y');

alter table covidvaccinations drop column date;

alter table covidvaccinations rename column dates to date;

select * from covidvaccinations order by date;

commit;

# Top 5 countries with highest death percentage to cases

desc coviddeaths;

select location,max(total_cases) as 'Total Cases',max(total_deaths) as 'Total Deaths',round((max(total_deaths)/max(total_cases)*100),2) as 'Death percent' from coviddeaths group by location order by max(total_deaths)/max(total_cases) desc limit 5;

desc covidvaccinations;

#Vaccination percentage by country

select dth.location, (max(vac.people_vaccinated)/max(dth.population))*100 as 'Vaccination Percentage' from coviddeaths dth join covidvaccinations vac on
dth.location=vac.location and dth.date=vac.date group by dth.location order by max(vac.people_vaccinated)/max(dth.population) desc;

# Top countires with the highest infection rate to population

SELECT 
    location, max(population) as 'Total Population', (max(total_cases) / max(population)) * 100 as 'Infection percentage'
FROM
    coviddeaths
GROUP BY location
ORDER BY max(total_cases) / max(population) DESC
LIMIT 5;

#Global trends day wise

select date,sum(new_cases) as 'New Cases',sum(new_deaths) 'New Deaths', (sum(new_deaths)/sum(new_cases))*100 as 'Death Percentage'
from coviddeaths group by date order by 1;

#cumulative new vaccines day wise per country

with vaccinations_cte as
(select vac.location,dth.population, dth.date, vac.new_vaccinations,sum(vac.new_vaccinations) over(partition by vac.location order by dth.location,dth.date) as Rolling_Vaccination 
from coviddeaths dth 
join covidvaccinations vac 
on vac.date=dth.date and vac.location=dth.location)
select *,(Rolling_Vaccination/population)*100 from vaccinations_cte;

#Same with Temp table
create temporary table rolling_vac(select vac.location,dth.population, dth.date, vac.new_vaccinations,sum(vac.new_vaccinations) over(partition by vac.location order by dth.location,dth.date) as Rolling_Vaccination 
from coviddeaths dth 
join covidvaccinations vac 
on vac.date=dth.date and vac.location=dth.location);

select *,(Rolling_Vaccination/population)*100 as Rolloing_vaccination_percentage from rolling_vac;

#Creating view to store data for later visualizations

create view rolling_vacciation as (
select vac.location,dth.population, dth.date, vac.new_vaccinations,sum(vac.new_vaccinations) over(partition by vac.location order by dth.location,dth.date) as Rolling_Vaccination 
from coviddeaths dth 
join covidvaccinations vac 
on vac.date=dth.date and vac.location=dth.location
);

select * from rolling_vacciation;





desc coviddeaths;
desc covidvaccinations;