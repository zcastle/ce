BEGIN;
CREATE TABLE `main_pais` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `no_pais` varchar(100) NOT NULL
)
;
CREATE TABLE `main_empresa` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `im_logo` varchar(100) NOT NULL,
    `nu_ruc` varchar(11) NOT NULL UNIQUE,
    `no_razon_social` varchar(255) NOT NULL UNIQUE,
    `no_comercial` varchar(255) NOT NULL,
    `de_direccion` longtext NOT NULL,
    `pais_id` integer NOT NULL,
    `ubigeo_id` integer NOT NULL,
    `nu_fijo` varchar(50) NOT NULL,
    `nu_movil` varchar(50) NOT NULL,
    `no_web` varchar(200) NOT NULL,
    `no_contacto` varchar(255) NOT NULL,
    `nu_telefono_contacto` varchar(50) NOT NULL,
    `no_email_contacto` varchar(255),
    `fl_notificaciones` bool NOT NULL,
    `user_id` integer NOT NULL UNIQUE
)
;
ALTER TABLE `main_empresa` ADD CONSTRAINT `pais_id_refs_id_27ffdb7e` FOREIGN KEY (`pais_id`) REFERENCES `main_pais` (`id`);
ALTER TABLE `main_empresa` ADD CONSTRAINT `ubigeo_id_refs_id_40f08a1c` FOREIGN KEY (`ubigeo_id`) REFERENCES `ubigeo_ubigeo` (`id`);
ALTER TABLE `main_empresa` ADD CONSTRAINT `user_id_refs_id_6e9a70e7` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
CREATE TABLE `main_area` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `no_area` varchar(50) NOT NULL
)
;
CREATE TABLE `main_tipoempleo` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `no_tipo_empleo` varchar(50) NOT NULL UNIQUE
)
;
CREATE TABLE `main_universidad` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `no_universidad` varchar(255) NOT NULL UNIQUE
)
;
CREATE TABLE `main_carrera` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `no_carrera` varchar(255) NOT NULL UNIQUE
)
;
CREATE TABLE `main_empleoestado` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `no_estado` varchar(50) NOT NULL UNIQUE
)
;
CREATE TABLE `main_preguntas` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `no_pregunta` varchar(255) NOT NULL
)
;
CREATE TABLE `main_empleo_preguntas` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `empleo_id` integer NOT NULL,
    `preguntas_id` integer NOT NULL,
    UNIQUE (`empleo_id`, `preguntas_id`)
)
;
ALTER TABLE `main_empleo_preguntas` ADD CONSTRAINT `preguntas_id_refs_id_7810021` FOREIGN KEY (`preguntas_id`) REFERENCES `main_preguntas` (`id`);
CREATE TABLE `main_empleo` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `no_empleo` varchar(255) NOT NULL,
    `de_empleo` longtext NOT NULL,
    `no_contacto` varchar(100) NOT NULL,
    `no_contacto_telefono` varchar(50) NOT NULL,
    `no_contacto_email` varchar(255) NOT NULL,
    `de_requisitos` longtext NOT NULL,
    `de_funciones` longtext NOT NULL,
    `va_sueldo` numeric(10, 2) NOT NULL,
    `fe_creacion` datetime NOT NULL,
    `fe_modificacion` datetime NOT NULL,
    `area_id` integer NOT NULL,
    `tipoempleo_id` integer NOT NULL,
    `ubigeo_id` integer NOT NULL,
    `estado_id` integer NOT NULL,
    `user_id` integer NOT NULL
)
;
ALTER TABLE `main_empleo` ADD CONSTRAINT `area_id_refs_id_8bb8160` FOREIGN KEY (`area_id`) REFERENCES `main_area` (`id`);
ALTER TABLE `main_empleo` ADD CONSTRAINT `user_id_refs_id_1edfe6e3` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `main_empleo` ADD CONSTRAINT `ubigeo_id_refs_id_eabf2e8` FOREIGN KEY (`ubigeo_id`) REFERENCES `ubigeo_ubigeo` (`id`);
ALTER TABLE `main_empleo` ADD CONSTRAINT `tipoempleo_id_refs_id_6eb77011` FOREIGN KEY (`tipoempleo_id`) REFERENCES `main_tipoempleo` (`id`);
ALTER TABLE `main_empleo` ADD CONSTRAINT `estado_id_refs_id_6f623fe5` FOREIGN KEY (`estado_id`) REFERENCES `main_empleoestado` (`id`);
ALTER TABLE `main_empleo_preguntas` ADD CONSTRAINT `empleo_id_refs_id_a4f9481` FOREIGN KEY (`empleo_id`) REFERENCES `main_empleo` (`id`);
CREATE TABLE `main_estadocivil` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `no_estado_civil` varchar(255) NOT NULL
)
;
CREATE TABLE `main_sexo` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `fl_Sexo` varchar(255) NOT NULL
)
;
CREATE TABLE `main_tipolicencia` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `no_tipo_licencia` varchar(255) NOT NULL
)
;
CREATE TABLE `main_postulante` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `im_foto` varchar(100) NOT NULL,
    `no_postulante` varchar(255) NOT NULL,
    `ap_postulante` varchar(255) NOT NULL,
    `am_postulante` varchar(255) NOT NULL,
    `fe_nacimiento` date NOT NULL,
    `sexo_id` integer NOT NULL,
    `de_direccion` longtext NOT NULL,
    `pais_id` integer NOT NULL,
    `ubigeo_id` integer NOT NULL,
    `nu_fijo` varchar(50) NOT NULL,
    `nu_movil` varchar(50) NOT NULL,
    `estadocivil_id` integer NOT NULL,
    `fl_licencia` bool NOT NULL,
    `tipolicencia_id` integer,
    `fl_auto_propio` bool NOT NULL,
    `de_sobremi` longtext NOT NULL,
    `fl_notificaciones` bool NOT NULL,
    `user_id` integer NOT NULL UNIQUE
)
;
ALTER TABLE `main_postulante` ADD CONSTRAINT `pais_id_refs_id_f9d0b35` FOREIGN KEY (`pais_id`) REFERENCES `main_pais` (`id`);
ALTER TABLE `main_postulante` ADD CONSTRAINT `tipolicencia_id_refs_id_36bd3db6` FOREIGN KEY (`tipolicencia_id`) REFERENCES `main_tipolicencia` (`id`);
ALTER TABLE `main_postulante` ADD CONSTRAINT `user_id_refs_id_636ece28` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `main_postulante` ADD CONSTRAINT `sexo_id_refs_id_4dc8ca87` FOREIGN KEY (`sexo_id`) REFERENCES `main_sexo` (`id`);
ALTER TABLE `main_postulante` ADD CONSTRAINT `ubigeo_id_refs_id_460098a3` FOREIGN KEY (`ubigeo_id`) REFERENCES `ubigeo_ubigeo` (`id`);
ALTER TABLE `main_postulante` ADD CONSTRAINT `estadocivil_id_refs_id_7bb95298` FOREIGN KEY (`estadocivil_id`) REFERENCES `main_estadocivil` (`id`);
CREATE TABLE `main_postulanteempresaempleo` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `empleo_id` integer NOT NULL,
    `user_id` integer NOT NULL,
    `fe_creacion` datetime NOT NULL
)
;
ALTER TABLE `main_postulanteempresaempleo` ADD CONSTRAINT `empleo_id_refs_id_48adbc68` FOREIGN KEY (`empleo_id`) REFERENCES `main_empleo` (`id`);
ALTER TABLE `main_postulanteempresaempleo` ADD CONSTRAINT `user_id_refs_id_251ee55a` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
CREATE TABLE `main_postulanteestudio` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `institucion_id` integer NOT NULL,
    `carrera_id` integer NOT NULL,
    `fe_periodo_ini` varchar(7) NOT NULL,
    `fe_periodo_fin` varchar(7) NOT NULL,
    `fl_actualidad` bool NOT NULL,
    `user_id` integer NOT NULL
)
;
ALTER TABLE `main_postulanteestudio` ADD CONSTRAINT `institucion_id_refs_id_50a80c17` FOREIGN KEY (`institucion_id`) REFERENCES `main_universidad` (`id`);
ALTER TABLE `main_postulanteestudio` ADD CONSTRAINT `carrera_id_refs_id_2336952d` FOREIGN KEY (`carrera_id`) REFERENCES `main_carrera` (`id`);
ALTER TABLE `main_postulanteestudio` ADD CONSTRAINT `user_id_refs_id_67a792bc` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
CREATE TABLE `main_postulanteempleo` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `no_empresa` varchar(255) NOT NULL,
    `no_cargo` varchar(255) NOT NULL,
    `de_funciones` longtext NOT NULL,
    `de_logros` longtext NOT NULL,
    `no_referencia` varchar(255) NOT NULL,
    `no_referencia_cargo` varchar(255) NOT NULL,
    `nu_referencia_telefono` varchar(255) NOT NULL,
    `fe_periodo_ini` varchar(7) NOT NULL,
    `fe_periodo_fin` varchar(7) NOT NULL,
    `fl_actualidad` bool NOT NULL,
    `user_id` integer NOT NULL
)
;
ALTER TABLE `main_postulanteempleo` ADD CONSTRAINT `user_id_refs_id_37b958f0` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
CREATE TABLE `main_mensajedirecto` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `fe_creacion` datetime NOT NULL,
    `de_asunto` varchar(255) NOT NULL,
    `de_mensaje` longtext NOT NULL,
    `de_adjunto` varchar(100) NOT NULL,
    `fl_revisado` bool NOT NULL,
    `fe_revisado` datetime,
    `remitente_id` integer NOT NULL,
    `destinatario_id` integer NOT NULL,
    `postulanteempresaempleo_id` integer NOT NULL
)
;
ALTER TABLE `main_mensajedirecto` ADD CONSTRAINT `postulanteempresaempleo_id_refs_id_205e501d` FOREIGN KEY (`postulanteempresaempleo_id`) REFERENCES `main_postulanteempresaempleo` (`id`);
ALTER TABLE `main_mensajedirecto` ADD CONSTRAINT `remitente_id_refs_id_7281566e` FOREIGN KEY (`remitente_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `main_mensajedirecto` ADD CONSTRAINT `destinatario_id_refs_id_7281566e` FOREIGN KEY (`destinatario_id`) REFERENCES `auth_user` (`id`);
CREATE TABLE `main_idioma` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `no_idioma` varchar(255) NOT NULL
)
;
CREATE TABLE `main_nivel` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `no_nivel` varchar(255) NOT NULL
)
;
CREATE TABLE `main_postulanteidiomanivel` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL,
    `idioma_id` integer NOT NULL,
    `nivel_id` integer NOT NULL
)
;
ALTER TABLE `main_postulanteidiomanivel` ADD CONSTRAINT `idioma_id_refs_id_433c2bb` FOREIGN KEY (`idioma_id`) REFERENCES `main_idioma` (`id`);
ALTER TABLE `main_postulanteidiomanivel` ADD CONSTRAINT `nivel_id_refs_id_157cd97b` FOREIGN KEY (`nivel_id`) REFERENCES `main_nivel` (`id`);
ALTER TABLE `main_postulanteidiomanivel` ADD CONSTRAINT `user_id_refs_id_3f7611e8` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
CREATE TABLE `main_recuperarpassword` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `usuario` varchar(255) NOT NULL,
    `email` varchar(255) NOT NULL,
    `token` varchar(255) NOT NULL UNIQUE,
    `fe_expira` datetime NOT NULL,
    `fl_usado` bool NOT NULL
)
;
CREATE TABLE `main_programa` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `no_programa` varchar(255) NOT NULL
)
;
CREATE TABLE `main_postulanteprogramanivel` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL,
    `programa_id` integer NOT NULL,
    `nivel_id` integer NOT NULL
)
;
ALTER TABLE `main_postulanteprogramanivel` ADD CONSTRAINT `programa_id_refs_id_f43ff73` FOREIGN KEY (`programa_id`) REFERENCES `main_programa` (`id`);
ALTER TABLE `main_postulanteprogramanivel` ADD CONSTRAINT `nivel_id_refs_id_7f82b4b3` FOREIGN KEY (`nivel_id`) REFERENCES `main_nivel` (`id`);
ALTER TABLE `main_postulanteprogramanivel` ADD CONSTRAINT `user_id_refs_id_19b6bfea` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;
