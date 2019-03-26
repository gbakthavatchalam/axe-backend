-- ****************** SqlDBM: MySQL ******************;
-- ***************************************************;

-- ************************************** database
USE gbakthavatchalam$axe;
-- ************************************** `user`


-- ************************************** `event`

CREATE TABLE `event`
(
 `id`          bigint NOT NULL AUTO_INCREMENT,
 `name`        varchar(200) NOT NULL ,
 `description` text NOT NULL ,
 `start_date`  datetime NOT NULL ,
 `end_date`    datetime NOT NULL ,
 `host`        int NOT NULL ,
 `location`    varchar(100) NOT NULL,
PRIMARY KEY (`id`),
KEY `fkIdx_14` (`host`),
CONSTRAINT `FK_14` FOREIGN KEY `fkIdx_14` (`host`) REFERENCES `auth_user` (`id`)
);

-- ************************************** `acceptance`

CREATE TABLE `acceptance`
(
 `id`          bigint NOT NULL AUTO_INCREMENT,
 `event_id`    bigint NOT NULL ,
 `response`    int ,
 `participant` int NOT NULL ,
PRIMARY KEY (`id`),
KEY `fkIdx_20` (`event_id`),
CONSTRAINT `FK_20` FOREIGN KEY `fkIdx_20` (`event_id`) REFERENCES `event` (`id`),
KEY `fkIdx_25` (`participant`),
CONSTRAINT `FK_25` FOREIGN KEY `fkIdx_25` (`participant`) REFERENCES `auth_user` (`id`)
);
