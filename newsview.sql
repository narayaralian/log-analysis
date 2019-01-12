CREATE OR REPLACE VIEW author_view
    AS SELECT articles.author, SUM(log.views) AS views
    FROM articles INNER JOIN (
        SELECT log.path, COUNT(log.path) AS views
        FROM log GROUP BY log.path
    ) AS log
    ON CONCAT('/article/', articles.slug) = log.path
    GROUP BY articles.author
    ORDER BY views DESC;


CREATE OR REPLACE VIEW date_total
    AS SELECT time::date AS date,
    COUNT(status)::float AS total
    FROM log GROUP BY date;


CREATE OR REPLACE VIEW date_error
    AS SELECT time::date AS date,
    COUNT(status)::float AS error
    FROM log
    WHERE status = '404 NOT FOUND'
    GROUP BY date;