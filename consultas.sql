--Query
CREATE TABLE cat.adipy (
	int_id SERIAL PRIMARY KEY,
	var_nombre VARCHAR(30) NOT NULL,
	var_ip VARCHAR(20) NOT NULL,
	int_puerto INTEGER NOT NULL,
	var_ruta VARCHAR,
	int_idusuario_modificacion INTEGER NOT NULL,
	int_idusuario_registro INTEGER NOT NULL,
	dt_modificacion TIMESTAMP WITHOUT TIME ZONE,
	dt_registro TIMESTAMP WITHOUT TIME ZONE,
	bol_enuso BOOLEAN DEFAULT TRUE
);

CREATE TABLE cat.usuario
(
	int_id_usuario serial primary key NOT NULL,
	int_id_perfil integer NOT NULL,
	int_id_distribuidor integer, -- solo para el perfil 2, puede ser nulo
	var_nombre character varying NOT NULL,
	var_apellidos character varying NOT NULL,
	var_correo character varying NOT NULL,
	var_usuario character varying NOT NULL,
	bta_password bytea NOT NULL,
	dt_fecha_registro timestamp without time zone NOT NULL,
	dt_fecha_modificado timestamp without time zone NOT NULL,
	bol_enuso boolean NOT NULL
);

SELECT * FROM cat.usuario(
	int_id SERIAL PRIMARY KEY,
	var_nombre VARCHAR(30) NOT NULL,
	var_apellidos VARCHAR(30) NOT NULL,
	var_correo VARCHAR() NOT NULL
);
