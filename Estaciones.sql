insert into dosificacion_linea (`nombreLinea`,`colorLinea`,`no_estaciones`) values
('Linea 1', 'Rosa', 20),
('Linea 2', 'Azul', 0),
('Linea 3', 'Verde Olivo', 0),
('Linea 4', 'Cian', 0),
('Linea 5', 'Amarillo', 0),
('Linea 6', 'Rojo', 0),
('Linea 7', 'Naranja', 0),
('Linea 8', 'Verde', 0),
('Linea 9', 'Cafe', 0),
('Linea A', 'Morado', 0),
('Linea B', 'Verde/Gris', 0),
('Linea 12', 'Oro', 0);

insert into dosificacion_estaciones(`estacion`,`statusSistema`,`id_linea_id`) 
values 
('Pantitlan',0,1),
('Zaragoza',0,1),
('Gomez Farias',0,1),
('Blvd. Puerto areo',0,1),
('Balbuena',0,1),
('Moctezuma',0,1),
('San lazaro',0,1),
('Cancelaria',0,1),
('Merced',0,1),
('Pino suarez',0,1),
('Isabel la catolica',0,1),
('Salto del agua',0,1),
('Balderas',0,1),
('Cuahutemoc',0,1),
('Insurgentes',0,1),
('Sevilla',0,1),
('Chapultepec',0,1),
('Juanacatlan',0,1),
('Tacubaya',0,1),
('Observatorio',0,1);

INSERT INTO `dosificacion_historicoafluencia` (`fecha`, `conteo`, `id_estacion_id`) VALUES
('2020-12-12 15:00:00.000000', 100, 1),
('2020-12-12 15:05:00.000000', 100, 1),
('2020-12-12 15:10:00.000000', 10, 1),
('2020-12-12 15:15:00.000000', 100, 1),
('2020-12-12 16:20:00.000000', 100, 1),
('2020-12-12 16:15:00.000000', 100, 1),
('2020-12-12 16:30:00.000000', 100, 1),
('2020-12-12 16:45:00.000000', 80, 1),
('2020-12-12 17:00:00.000000', 21, 1),
('2020-12-19 16:00:00.000000', 86, 2),
('2020-12-19 16:05:00.000000', 41, 2),
('2020-12-19 16:10:00.000000', 21, 2),
('2020-12-19 16:15:00.000000', 12, 2),
('2020-12-19 16:20:00.000000', 91, 2),
('2020-12-19 16:25:00.000000', 74, 2),
('2020-12-19 16:30:00.000000', 100, 2),
('2020-12-13 18:15:00.000000', 100, 1),
('2020-12-19 16:45:00.000000', 0, 2),
('2020-12-19 16:50:00.000000', 30, 2),
('2020-12-19 16:55:00.000000', 50, 2),
('2020-12-19 17:00:00.000000', 49, 2),
('2020-12-19 17:05:00.000000', 12, 2),
('2020-12-19 17:10:00.000000', 33, 2),
('2020-12-19 17:10:00.000000', 33, 1),
('2020-12-19 17:15:00.000000', 33, 2),
('2020-12-19 17:10:00.000000', 33, 1),
('2020-12-19 17:25:00.000000', 13, 2),
('2020-12-19 17:20:00.000000', 33, 2),
('2020-12-19 17:10:00.000000', 33, 1),
('2020-12-19 17:30:00.000000', 13, 2),
('2020-12-19 17:10:00.000000', 33, 1);

INSERT INTO `dosificacion_trenes`(`fecha`, `conteoTrenes`, `id_estacion_id`) VALUES 
('2020-12-19',10,2),
('2020-12-20',8,2),
('2020-12-21',30,2),
('2020-12-22',15,2),
('2020-12-23',5,2),
('2020-12-24',2,2),
('2020-12-25',8,2);