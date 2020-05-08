Create database dosificacion_estacion;
use dosificacion_estacion

CREATE TABLE `historico` (
  `id` int(11) NOT NULL,
  `fecha` datetime NOT NULL,
  `valores` int(11) NOT NULL,
  `id_camara` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `historico`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `historico`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=166;
