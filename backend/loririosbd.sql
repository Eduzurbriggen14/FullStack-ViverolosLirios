DROP SCHEMA IF EXISTS liriosDB;
CREATE SCHEMA liriosDB;
USE liriosDB;

DROP TABLE IF EXISTS `empleado`;

CREATE TABLE `liriosDB`.`empleado` 
(`legajo` INT(10) NOT NULL AUTO_INCREMENT ,
 `nombre` VARCHAR(100) NOT NULL ,
 `apellido` VARCHAR(100) NOT NULL ,
 `rol` ENUM('vendedor','diseñador','jardinero','paisajista') NOT NULL ,
 PRIMARY KEY (`legajo`));


INSERT INTO `empleado` (`legajo`, `nombre`, `apellido`, `rol`) VALUES (NULL, 'Susana', 'Sanchez', 'vendedor');
COMMIT;

DROP TABLE IF EXISTS `cliente`;

CREATE TABLE `liriosDB`.`cliente` (
`dni` INT(10) NOT NULL ,
 `nombre` VARCHAR(100) NOT NULL ,
 `apellido` VARCHAR(100) NOT NULL ,
 `email` VARCHAR(100) NOT NULL ,
 `telefono` VARCHAR(20) NOT NULL ,
 PRIMARY KEY (`dni`)) ENGINE = InnoDB; 

INSERT INTO `cliente` (`dni`, `nombre`, `apellido`, `email`, `telefono`) VALUES (45682562, 'Juan', 'Rodriguez', 'juan@gmail.com', '11-555-5555');
COMMIT;

DROP TABLE IF EXISTS `producto`;

CREATE TABLE `liriosDB`.`producto` (
`codigo` INT(10) NOT NULL AUTO_INCREMENT,
`nombre` VARCHAR(100) NOT NULL ,
`descripcion` VARCHAR(150) NOT NULL , 
`precio` FLOAT(10) NOT NULL , 
`stock` INT(10) NOT NULL , 
`categoria` ENUM('lirios','herramientas','macetas','gromineas','frutales','fuentes') NOT NULL ,
`imagen` VARCHAR(100) NOT NULL, 
PRIMARY KEY (`codigo`))ENGINE = InnoDB; 
COMMIT;

INSERT INTO `liriosDB`.`producto` (`nombre`, `descripcion`, `precio`, `stock`, `categoria`, `imagen`) VALUES ('Lirio Azul', 'Hermosa flor de color azul', 9.99, 50, 'lirios', 'lirio_azul.jpg');

INSERT INTO `liriosDB`.`producto` (`nombre`, `descripcion`, `precio`, `stock`, `categoria`, `imagen`)  VALUES 
('Lirio Morado', 'Hermosa flor de color morado', 9.99, 10, 'lirios', 'lirio_morado.jpg'),
('Lirio Blanco', 'Hermosa flor de color blanco', 10.99, 50, 'lirios', 'lirio_blanco.jpg'),
('palita', 'palita para realizar trbajos de jardineria', 50, 30, 'herramientas', 'palita.jpg');

DROP TABLE IF EXISTS `consulta`;

CREATE TABLE `liriosDB`.`consulta` (
`id` INT(10) NOT NULL AUTO_INCREMENT , 
`nombre` VARCHAR(50) NOT NULL , 
`correo` VARCHAR(50) NOT NULL , 
`provincia` VARCHAR(30) NOT NULL , 
`ciudad` VARCHAR(30) NOT NULL , 
`mensaje` VARCHAR(250) NOT NULL , 
PRIMARY KEY (`id`)) ENGINE = InnoDB; 
COMMIT;