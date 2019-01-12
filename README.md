# Introduction to Logs Analysis

Log Analysis as a Python3 and PostgreSQL based **internal reporting tool** that analyzes data from a sample newspaper website database to provide basic statistics about the readers' preferences and the website's behavior.

Log Analysis will generate reports (in a simple html format) on:  
- the most popular three  articles on the website;  
- the most popular authors of all time;  
- the days when more than 1% of requests to webpages led to an error.

*Note*: Log Analysis is not a real-world project. It was developed for learning purposes only. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

To be able to run Log Analysis, you need a Linux-based virtual machine (VM) installed on your local machine. 
You can use Vagrant and VirtualBox to install and manage the VM:

1. Download [VirtualBox from virtualbox.org](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1). Install the platform package for your operating system.
  
2. Download [Vagrant from vagrantup.com](https://www.vagrantup.com/downloads.html). Install the version for your operating system.  
If Vagrant is successfully installed, you will be able to run `vagrant --version` in your terminal to see the version number.

3. On your local machine, create a vagrant directory for the project; unzip the content of this folder into that directory. You will end up with a directory containing the following files:     
news.py, newsdata.sql, newsview.sql, Vagrantfile, README.md
- In your terminal, cd to your vagrant directory.

4. Start the virtual machine:  
- From your terminal, inside the vagrant directory, run the command `vagrant up`. Wait until the command is finished running (this may take a while...).
- When `vagrant up` is finished running, you will get your shell prompt back. At this point, you can run `vagrant ssh` to log in to your Linux VM. 


### Installing Log Analysis

Create a local copy of the sample newspaper database and populate it with data:
- cd into the vagrant directory and use the command `psql create database news` to create a new database called *news*;   
- use the command `psql -d news -f newsdata.sql` to load the site's data into your local database;
- use the command `psql -d news -f newsview.sql` to add VIEWs to the database.
- connect to your database using `psql -d news`; use the \dt and \d table commands and select statements to explore the tables.


### Project design
All the database-related functionality is implemented in newsdb.py using three functions: pop_articles(), pop_authors(), and status_check().

**pop_articles()** - returns the title and the number of views for the three most popular articles by matching data from two tables: articles.slug and log.path;
**pop_authors()** - returns the names of authors and the numbers of views for each author's articles ordered by the number of views by matching data from authors.name and log.path  
*Note* this function uses a VIEW table (author_view):

```sql
CREATE OR REPLACE VIEW author_view
    AS SELECT articles.author, SUM(log.views) AS views
    FROM articles INNER JOIN (
        SELECT log.path, COUNT(log.path) AS views
        FROM log GROUP BY log.path
    ) AS log
    ON CONCAT('/article/', articles.slug) = log.path
    GROUP BY articles.author
    ORDER BY views DESC;
```  

**status_check()** - returns percent of "bad" requests for the days when more than 1% of requests led to error
*Note* this function uses two VIEW tables (date_total, date_error):

*date_total*
```sql
CREATE OR REPLACE VIEW date_total
    AS SELECT time::date AS date,
    COUNT(status)::float AS total
    FROM log GROUP BY date;
```

*date_error*
```sql
CREATE OR REPLACE VIEW date_error
    AS SELECT time::date AS date,
    COUNT(status)::float AS error
    FROM log
    WHERE status = '404 NOT FOUND'
    GROUP BY date;
```


## Running the tests

### How to run the application

- from the terminal, use the command `python news.py` to run the application;


## Deployment

Log Analysis was developed for learning purposes only and is not intended to be deployed on a live system.

## Built With

* [Python 3](https://www.python.org/)
* [PostgreSQL](https://www.postgresql.org/)

## Authors

* **Nara Yaralyan** - [LinkedIn](https://www.linkedin.com/in/nara-yaralyan-0b35a833/)

## License

This project is licensed under the MIT License.

## Acknowledgments

* This tool was developed as part of the Udacity Full-Stack Web Development Program. Many thanks to the Udacity team for such a great program!