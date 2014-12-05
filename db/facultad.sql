BEGIN TRANSACTION;
CREATE TABLE `facultad` (
    `id`     INTEGER,
    `nombre` TEXT,
    PRIMARY KEY(id)
);
CREATE TABLE `empadronado` (
    `dni`                 INTEGER,
    `nombre`              TEXT,
    `fecha_de_nacimiento` INTEGER,
    `id_facultad`         INTEGER,
    `claustro`                INTEGER,
    PRIMARY KEY(dni),
    FOREIGN KEY(id_facultad) REFERENCES facultad(id)
);
CREATE TABLE `estudiante` (
    `dni`               INTEGER,
    `fecha_inscripcion` INTEGER,
    PRIMARY KEY(dni),
    FOREIGN KEY(dni) REFERENCES empadronado(dni) ON DELETE CASCADE
);
CREATE TABLE `graduado` (
    `dni`  INTEGER,
    `universidad` INTEGER,
    PRIMARY KEY(dni),
    FOREIGN KEY(dni) REFERENCES empadronado(dni) ON DELETE CASCADE
);
CREATE TABLE `graduado_otra_universidad` (
    `dni`                INTEGER,
    `inicio_actividades` INTEGER,
    PRIMARY KEY(dni),
    FOREIGN KEY(dni) REFERENCES graduado(dni) ON DELETE CASCADE
);
CREATE TABLE `profesor` (
    `dni`                      INTEGER,
    `nacionalidad_universidad` TEXT,
    PRIMARY KEY(dni),
    FOREIGN KEY(dni) REFERENCES empadronado(dni) ON DELETE CASCADE
);
CREATE TABLE `calendario_electoral` (
    `periodo` INTEGER,
    PRIMARY KEY(periodo)
);
CREATE TABLE `agrupacion_politica` (
    `id`     INTEGER,
    `nombre` TEXT,
    PRIMARY KEY(id)
);
CREATE TABLE `agrupacion_politica_se_presenta_durante_calendario_electoral` (
    `id_agrupacion_politica` INTEGER,
    `periodo`                  INTEGER,
    `votos_recibidos`        INTEGER,
    PRIMARY KEY(id_agrupacion_politica, periodo),
    FOREIGN KEY(id_agrupacion_politica) REFERENCES agrupacion_politica(id),
    FOREIGN KEY(periodo) REFERENCES calendario_electoral(periodo)
);
CREATE TABLE `consejero_directivo` (
    `dni`                    INTEGER,
    `periodo`                INTEGER,
    `id_agrupacion_politica` INTEGER,
    `claustro`                   INTEGER,
    PRIMARY KEY(dni, periodo),
    FOREIGN KEY(dni) REFERENCES empadronado(dni),
    FOREIGN KEY(id_agrupacion_politica) REFERENCES agrupacion_politica(id)
);
CREATE TABLE `decano` (
    `dni`     INTEGER,
    `periodo` INTEGER,
    PRIMARY KEY(dni, periodo),
    FOREIGN KEY(dni) REFERENCES profesor(dni)
);
CREATE TABLE `voto_a_decano` (
    `dni_decano`                  INTEGER,
    `periodo_decano`              INTEGER,
    `dni_consejero_directivo`     INTEGER,
    `periodo_consejero_directivo` INTEGER,
    PRIMARY KEY(dni_decano, periodo_decano, dni_consejero_directivo, periodo_consejero_directivo),
    FOREIGN KEY(dni_decano, periodo_decano) REFERENCES decano(dni, periodo),
    FOREIGN KEY(dni_consejero_directivo, periodo_consejero_directivo) REFERENCES consejero_directivo(dni, periodo)
);
CREATE TABLE `consejero_superior` (
    `dni`                    INTEGER,
    `periodo`                INTEGER,
    `claustro`                   INTEGER,
    PRIMARY KEY(dni, periodo),
    FOREIGN KEY(dni) REFERENCES empadronado(dni)
);
CREATE TABLE `voto_a_consejero_superior` (
    `dni_consejero_superior`      INTEGER,
    `periodo_consejero_superior`  INTEGER,
    `dni_consejero_directivo`     INTEGER,
    `periodo_consejero_directivo` INTEGER,
    PRIMARY KEY(dni_consejero_superior, periodo_consejero_superior, dni_consejero_directivo, periodo_consejero_directivo),
    FOREIGN KEY(dni_consejero_superior, periodo_consejero_superior) REFERENCES consejero_superior(dni, periodo),
    FOREIGN KEY(dni_consejero_directivo, periodo_consejero_directivo) REFERENCES consejero_directivo(dni, periodo)
);
CREATE TABLE `rector` (
    `dni`     INTEGER,
    `periodo` INTEGER,
    PRIMARY KEY(dni, periodo),
    FOREIGN KEY(dni) REFERENCES profesor(dni)
);
CREATE TABLE `rector_fue_votado_por_consejero_directivo` (
    `dni_rector`                  INTEGER,
    `periodo_rector`              INTEGER,
    `dni_consejero_directivo`     INTEGER,
    `periodo_consejero_directivo` INTEGER,
    PRIMARY KEY(dni_rector, periodo_rector, dni_consejero_directivo, periodo_consejero_directivo),
    FOREIGN KEY(dni_rector, periodo_rector) REFERENCES rector(dni, periodo),
    FOREIGN KEY(dni_consejero_directivo, periodo_consejero_directivo) REFERENCES consejero_directivo(dni, periodo)
);
CREATE TABLE `rector_fue_votado_por_decano` (
    `dni_rector`     INTEGER,
    `periodo_rector` INTEGER,
    `dni_decano`     INTEGER,
    `periodo_decano` INTEGER,
    PRIMARY KEY(dni_rector, periodo_rector, dni_decano, periodo_decano),
    FOREIGN KEY(dni_rector, periodo_rector) REFERENCES rector(dni, periodo),
    FOREIGN KEY(dni_decano, periodo_decano) REFERENCES decano(dni, periodo)
);
CREATE TABLE `rector_fue_votado_por_consejero_superior` (
    `dni_rector`                 INTEGER,
    `periodo_rector`             INTEGER,
    `dni_consejero_superior`     INTEGER,
    `periodo_consejero_superior` INTEGER,
    PRIMARY KEY(dni_rector, periodo_rector, dni_consejero_superior, periodo_consejero_superior),
    FOREIGN KEY(dni_rector, periodo_rector) REFERENCES rector(dni, periodo),
    FOREIGN KEY(dni_consejero_superior, periodo_consejero_superior) REFERENCES consejero_superior(dni, periodo)
);
COMMIT;
PRAGMA foreign_keys = 1;
