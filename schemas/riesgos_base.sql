-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 24-10-2020 a las 01:40:19
-- Versión del servidor: 10.4.14-MariaDB
-- Versión de PHP: 7.2.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `db03student1151381`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `actividad`
--

CREATE TABLE `actividad` (
  `actividad_id` varchar(45) CHARACTER SET utf8 NOT NULL,
  `actividad_orden` int(11) NOT NULL,
  `actividad_uuid` int(11) NOT NULL,
  `actividad_nombre` varchar(100) NOT NULL,
  `actividad_level` int(11) DEFAULT NULL,
  `actividad_wbs` varchar(100) DEFAULT NULL,
  `proyecto_id` int(11) NOT NULL,
  `proyecto_linea_base` int(11) NOT NULL,
  `actividad_fecha_inicio` datetime DEFAULT NULL,
  `actividad_fecha_fin` datetime DEFAULT NULL,
  `duracion` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categoria`
--

CREATE TABLE `categoria` (
  `categoria_id` int(11) NOT NULL,
  `categoria_nombre` varchar(45) DEFAULT NULL,
  `categoria_descripcion` text DEFAULT NULL,
  `categoria_default` tinyint(4) NOT NULL DEFAULT 1,
  `categoria_uid` bigint(20) UNSIGNED DEFAULT NULL,
  `rbs_id` int(11) NOT NULL,
  `proyecto_linea_base` int(11) NOT NULL,
  `proyecto_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clasificacion_riesgo`
--

CREATE TABLE `clasificacion_riesgo` (
  `clasificacion_riesgo_id` int(11) NOT NULL,
  `clasificacion_riesgo_nombre` varchar(70) NOT NULL,
  `clasificacion_riesgo_min` int(11) NOT NULL,
  `clasificacion_riesgo_max` int(11) NOT NULL,
  `clasificacion_color` varchar(45) NOT NULL,
  `proyecto_id` int(11) NOT NULL,
  `proyecto_linea_base` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gerente`
--

CREATE TABLE `gerente` (
  `gerente_id` int(11) NOT NULL,
  `proyecto_linea_base` int(11) NOT NULL,
  `gerente_nombre` varchar(100) DEFAULT NULL,
  `gerente_usuario` varchar(45) NOT NULL,
  `gerente_correo` varchar(100) DEFAULT NULL,
  `gerente_fecha_creacion` datetime DEFAULT current_timestamp(),
  `gerente_profesion` varchar(100) DEFAULT NULL,
  `gerente_empresa` varchar(100) DEFAULT NULL,
  `gerente_metodologias` tinytext DEFAULT NULL,
  `gerente_certificaciones` tinytext DEFAULT NULL,
  `sector_id` int(11) NOT NULL,
  `pais_id` int(11) NOT NULL,
  `proyecto_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `impacto`
--

CREATE TABLE `impacto` (
  `impacto_id` int(11) NOT NULL,
  `impacto_categoria` varchar(70) NOT NULL,
  `impacto_valor` int(11) NOT NULL,
  `proyecto_id` int(11) NOT NULL,
  `proyecto_linea_base` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `leccion`
--

CREATE TABLE `leccion` (
  `leccion_id` int(11) NOT NULL,
  `leccion_descripcion` text NOT NULL,
  `proyecto_id` int(11) NOT NULL,
  `proyecto_linea_base` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pais`
--

CREATE TABLE `pais` (
  `pais_id` int(11) NOT NULL,
  `pais_nombre` varchar(100) DEFAULT NULL,
  `pais_name` varchar(100) NOT NULL,
  `pais_nom` varchar(100) NOT NULL,
  `pais_iso_2` varchar(45) DEFAULT NULL,
  `pais_iso_3` varchar(45) DEFAULT NULL,
  `pais_phone_code` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


INSERT INTO `pais` (`pais_id`, `pais_nombre`, `pais_name`, `pais_nom`, `pais_iso_2`, `pais_iso_3`, `pais_phone_code`) VALUES
(1, 'Afganistán', 'Afghanistan', 'Afghanistan', 'AF', 'AFG', '93'),
(2, 'Albania', 'Albania', 'Albanie', 'AL', 'ALB', '355'),
(3, 'Alemania', 'Germany', 'Allemagne', 'DE', 'DEU', '49'),
(4, 'Andorra', 'Andorra', 'Andorra', 'AD', 'AND', '376'),
(5, 'Angola', 'Angola', 'Angola', 'AO', 'AGO', '244'),
(6, 'Anguila', 'Anguilla', 'Anguilla', 'AI', 'AIA', '1 264'),
(7, 'Antártida', 'Antarctica', 'L\'Antarctique', 'AQ', 'ATA', '672'),
(8, 'Antigua y Barbuda', 'Antigua and Barbuda', 'Antigua et Barbuda', 'AG', 'ATG', '1 268'),
(9, 'Arabia Saudita', 'Saudi Arabia', 'Arabie Saoudite', 'SA', 'SAU', '966'),
(10, 'Argelia', 'Algeria', 'Algérie', 'DZ', 'DZA', '213'),
(11, 'Argentina', 'Argentina', 'Argentine', 'AR', 'ARG', '54'),
(12, 'Armenia', 'Armenia', 'L\'Arménie', 'AM', 'ARM', '374'),
(13, 'Aruba', 'Aruba', 'Aruba', 'AW', 'ABW', '297'),
(14, 'Australia', 'Australia', 'Australie', 'AU', 'AUS', '61'),
(15, 'Austria', 'Austria', 'Autriche', 'AT', 'AUT', '43'),
(16, 'Azerbaiyán', 'Azerbaijan', 'L\'Azerbaïdjan', 'AZ', 'AZE', '994'),
(17, 'Bélgica', 'Belgium', 'Belgique', 'BE', 'BEL', '32'),
(18, 'Bahamas', 'Bahamas', 'Bahamas', 'BS', 'BHS', '1 242'),
(19, 'Bahrein', 'Bahrain', 'Bahreïn', 'BH', 'BHR', '973'),
(20, 'Bangladesh', 'Bangladesh', 'Bangladesh', 'BD', 'BGD', '880'),
(21, 'Barbados', 'Barbados', 'Barbade', 'BB', 'BRB', '1 246'),
(22, 'Belice', 'Belize', 'Belize', 'BZ', 'BLZ', '501'),
(23, 'Benín', 'Benin', 'Bénin', 'BJ', 'BEN', '229'),
(24, 'Bhután', 'Bhutan', 'Le Bhoutan', 'BT', 'BTN', '975'),
(25, 'Bielorrusia', 'Belarus', 'Biélorussie', 'BY', 'BLR', '375'),
(26, 'Birmania', 'Myanmar', 'Myanmar', 'MM', 'MMR', '95'),
(27, 'Bolivia', 'Bolivia', 'Bolivie', 'BO', 'BOL', '591'),
(28, 'Bosnia y Herzegovina', 'Bosnia and Herzegovina', 'Bosnie-Herzégovine', 'BA', 'BIH', '387'),
(29, 'Botsuana', 'Botswana', 'Botswana', 'BW', 'BWA', '267'),
(30, 'Brasil', 'Brazil', 'Brésil', 'BR', 'BRA', '55'),
(31, 'Brunéi', 'Brunei', 'Brunei', 'BN', 'BRN', '673'),
(32, 'Bulgaria', 'Bulgaria', 'Bulgarie', 'BG', 'BGR', '359'),
(33, 'Burkina Faso', 'Burkina Faso', 'Burkina Faso', 'BF', 'BFA', '226'),
(34, 'Burundi', 'Burundi', 'Burundi', 'BI', 'BDI', '257'),
(35, 'Cabo Verde', 'Cape Verde', 'Cap-Vert', 'CV', 'CPV', '238'),
(36, 'Camboya', 'Cambodia', 'Cambodge', 'KH', 'KHM', '855'),
(37, 'Camerún', 'Cameroon', 'Cameroun', 'CM', 'CMR', '237'),
(38, 'Canadá', 'Canada', 'Canada', 'CA', 'CAN', '1'),
(39, 'Chad', 'Chad', 'Tchad', 'TD', 'TCD', '235'),
(40, 'Chile', 'Chile', 'Chili', 'CL', 'CHL', '56'),
(41, 'China', 'China', 'Chine', 'CN', 'CHN', '86'),
(42, 'Chipre', 'Cyprus', 'Chypre', 'CY', 'CYP', '357'),
(43, 'Ciudad del Vaticano', 'Vatican City State', 'Cité du Vatican', 'VA', 'VAT', '39'),
(44, 'Colombia', 'Colombia', 'Colombie', 'CO', 'COL', '57'),
(45, 'Comoras', 'Comoros', 'Comores', 'KM', 'COM', '269'),
(46, 'República del Congo', 'Republic of the Congo', 'République du Congo', 'CG', 'COG', '242'),
(47, 'República Democrática del Congo', 'Democratic Republic of the Congo', 'République démocratique du Congo', 'CD', 'COD', '243'),
(48, 'Corea del Norte', 'North Korea', 'Corée du Nord', 'KP', 'PRK', '850'),
(49, 'Corea del Sur', 'South Korea', 'Corée du Sud', 'KR', 'KOR', '82'),
(50, 'Costa de Marfil', 'Ivory Coast', 'Côte-d\'Ivoire', 'CI', 'CIV', '225'),
(51, 'Costa Rica', 'Costa Rica', 'Costa Rica', 'CR', 'CRI', '506'),
(52, 'Croacia', 'Croatia', 'Croatie', 'HR', 'HRV', '385'),
(53, 'Cuba', 'Cuba', 'Cuba', 'CU', 'CUB', '53'),
(54, 'Curazao', 'Curaçao', 'Curaçao', 'CW', 'CWU', '5999'),
(55, 'Dinamarca', 'Denmark', 'Danemark', 'DK', 'DNK', '45'),
(56, 'Dominica', 'Dominica', 'Dominique', 'DM', 'DMA', '1 767'),
(57, 'Ecuador', 'Ecuador', 'Equateur', 'EC', 'ECU', '593'),
(58, 'Egipto', 'Egypt', 'Egypte', 'EG', 'EGY', '20'),
(59, 'El Salvador', 'El Salvador', 'El Salvador', 'SV', 'SLV', '503'),
(60, 'Emiratos Árabes Unidos', 'United Arab Emirates', 'Emirats Arabes Unis', 'AE', 'ARE', '971'),
(61, 'Eritrea', 'Eritrea', 'Erythrée', 'ER', 'ERI', '291'),
(62, 'Eslovaquia', 'Slovakia', 'Slovaquie', 'SK', 'SVK', '421'),
(63, 'Eslovenia', 'Slovenia', 'Slovénie', 'SI', 'SVN', '386'),
(64, 'España', 'Spain', 'Espagne', 'ES', 'ESP', '34'),
(65, 'Estados Unidos de América', 'United States of America', 'États-Unis d\'Amérique', 'US', 'USA', '1'),
(66, 'Estonia', 'Estonia', 'L\'Estonie', 'EE', 'EST', '372'),
(67, 'Etiopía', 'Ethiopia', 'Ethiopie', 'ET', 'ETH', '251'),
(68, 'Filipinas', 'Philippines', 'Philippines', 'PH', 'PHL', '63'),
(69, 'Finlandia', 'Finland', 'Finlande', 'FI', 'FIN', '358'),
(70, 'Fiyi', 'Fiji', 'Fidji', 'FJ', 'FJI', '679'),
(71, 'Francia', 'France', 'France', 'FR', 'FRA', '33'),
(72, 'Gabón', 'Gabon', 'Gabon', 'GA', 'GAB', '241'),
(73, 'Gambia', 'Gambia', 'Gambie', 'GM', 'GMB', '220'),
(74, 'Georgia', 'Georgia', 'Géorgie', 'GE', 'GEO', '995'),
(75, 'Ghana', 'Ghana', 'Ghana', 'GH', 'GHA', '233'),
(76, 'Gibraltar', 'Gibraltar', 'Gibraltar', 'GI', 'GIB', '350'),
(77, 'Granada', 'Grenada', 'Grenade', 'GD', 'GRD', '1 473'),
(78, 'Grecia', 'Greece', 'Grèce', 'GR', 'GRC', '30'),
(79, 'Groenlandia', 'Greenland', 'Groenland', 'GL', 'GRL', '299'),
(80, 'Guadalupe', 'Guadeloupe', 'Guadeloupe', 'GP', 'GLP', '590'),
(81, 'Guam', 'Guam', 'Guam', 'GU', 'GUM', '1 671'),
(82, 'Guatemala', 'Guatemala', 'Guatemala', 'GT', 'GTM', '502'),
(83, 'Guayana Francesa', 'French Guiana', 'Guyane française', 'GF', 'GUF', '594'),
(84, 'Guernsey', 'Guernsey', 'Guernesey', 'GG', 'GGY', '44'),
(85, 'Guinea', 'Guinea', 'Guinée', 'GN', 'GIN', '224'),
(86, 'Guinea Ecuatorial', 'Equatorial Guinea', 'Guinée Equatoriale', 'GQ', 'GNQ', '240'),
(87, 'Guinea-Bissau', 'Guinea-Bissau', 'Guinée-Bissau', 'GW', 'GNB', '245'),
(88, 'Guyana', 'Guyana', 'Guyane', 'GY', 'GUY', '592'),
(89, 'Haití', 'Haiti', 'Haïti', 'HT', 'HTI', '509'),
(90, 'Honduras', 'Honduras', 'Honduras', 'HN', 'HND', '504'),
(91, 'Hong kong', 'Hong Kong', 'Hong Kong', 'HK', 'HKG', '852'),
(92, 'Hungría', 'Hungary', 'Hongrie', 'HU', 'HUN', '36'),
(93, 'India', 'India', 'Inde', 'IN', 'IND', '91'),
(94, 'Indonesia', 'Indonesia', 'Indonésie', 'ID', 'IDN', '62'),
(95, 'Irán', 'Iran', 'Iran', 'IR', 'IRN', '98'),
(96, 'Irak', 'Iraq', 'Irak', 'IQ', 'IRQ', '964'),
(97, 'Irlanda', 'Ireland', 'Irlande', 'IE', 'IRL', '353'),
(98, 'Isla Bouvet', 'Bouvet Island', 'Bouvet Island', 'BV', 'BVT', NULL),
(99, 'Isla de Man', 'Isle of Man', 'Ile de Man', 'IM', 'IMN', '44'),
(100, 'Isla de Navidad', 'Christmas Island', 'Christmas Island', 'CX', 'CXR', '61'),
(101, 'Isla Norfolk', 'Norfolk Island', 'Île de Norfolk', 'NF', 'NFK', '672'),
(102, 'Islandia', 'Iceland', 'Islande', 'IS', 'ISL', '354'),
(103, 'Islas Bermudas', 'Bermuda Islands', 'Bermudes', 'BM', 'BMU', '1 441'),
(104, 'Islas Caimán', 'Cayman Islands', 'Iles Caïmans', 'KY', 'CYM', '1 345'),
(105, 'Islas Cocos (Keeling)', 'Cocos (Keeling) Islands', 'Cocos (Keeling', 'CC', 'CCK', '61'),
(106, 'Islas Cook', 'Cook Islands', 'Iles Cook', 'CK', 'COK', '682'),
(107, 'Islas de Åland', 'Åland Islands', 'Îles Åland', 'AX', 'ALA', '358'),
(108, 'Islas Feroe', 'Faroe Islands', 'Iles Féro', 'FO', 'FRO', '298'),
(109, 'Islas Georgias del Sur y Sandwich del Sur', 'South Georgia and the South Sandwich Islands', 'Géorgie du Sud et les Îles Sandwich du Sud', 'GS', 'SGS', '500'),
(110, 'Islas Heard y McDonald', 'Heard Island and McDonald Islands', 'Les îles Heard et McDonald', 'HM', 'HMD', NULL),
(111, 'Islas Maldivas', 'Maldives', 'Maldives', 'MV', 'MDV', '960'),
(112, 'Islas Malvinas', 'Falkland Islands (Malvinas)', 'Iles Falkland (Malvinas', 'FK', 'FLK', '500'),
(113, 'Islas Marianas del Norte', 'Northern Mariana Islands', 'Iles Mariannes du Nord', 'MP', 'MNP', '1 670'),
(114, 'Islas Marshall', 'Marshall Islands', 'Iles Marshall', 'MH', 'MHL', '692'),
(115, 'Islas Pitcairn', 'Pitcairn Islands', 'Iles Pitcairn', 'PN', 'PCN', '870'),
(116, 'Islas Salomón', 'Solomon Islands', 'Iles Salomon', 'SB', 'SLB', '677'),
(117, 'Islas Turcas y Caicos', 'Turks and Caicos Islands', 'Iles Turques et Caïques', 'TC', 'TCA', '1 649'),
(118, 'Islas Ultramarinas Menores de Estados Unidos', 'United States Minor Outlying Islands', 'États-Unis Îles mineures éloignées', 'UM', 'UMI', '246'),
(119, 'Islas Vírgenes Británicas', 'Virgin Islands', 'Iles Vierges', 'VG', 'VGB', '1 284'),
(120, 'Islas Vírgenes de los Estados Unidos', 'United States Virgin Islands', 'Îles Vierges américaines', 'VI', 'VIR', '1 340'),
(121, 'Israel', 'Israel', 'Israël', 'IL', 'ISR', '972'),
(122, 'Italia', 'Italy', 'Italie', 'IT', 'ITA', '39'),
(123, 'Jamaica', 'Jamaica', 'Jamaïque', 'JM', 'JAM', '1 876'),
(124, 'Japón', 'Japan', 'Japon', 'JP', 'JPN', '81'),
(125, 'Jersey', 'Jersey', 'Maillot', 'JE', 'JEY', '44'),
(126, 'Jordania', 'Jordan', 'Jordan', 'JO', 'JOR', '962'),
(127, 'Kazajistán', 'Kazakhstan', 'Le Kazakhstan', 'KZ', 'KAZ', '7'),
(128, 'Kenia', 'Kenya', 'Kenya', 'KE', 'KEN', '254'),
(129, 'Kirguistán', 'Kyrgyzstan', 'Kirghizstan', 'KG', 'KGZ', '996'),
(130, 'Kiribati', 'Kiribati', 'Kiribati', 'KI', 'KIR', '686'),
(131, 'Kuwait', 'Kuwait', 'Koweït', 'KW', 'KWT', '965'),
(132, 'Líbano', 'Lebanon', 'Liban', 'LB', 'LBN', '961'),
(133, 'Laos', 'Laos', 'Laos', 'LA', 'LAO', '856'),
(134, 'Lesoto', 'Lesotho', 'Lesotho', 'LS', 'LSO', '266'),
(135, 'Letonia', 'Latvia', 'La Lettonie', 'LV', 'LVA', '371'),
(136, 'Liberia', 'Liberia', 'Liberia', 'LR', 'LBR', '231'),
(137, 'Libia', 'Libya', 'Libye', 'LY', 'LBY', '218'),
(138, 'Liechtenstein', 'Liechtenstein', 'Liechtenstein', 'LI', 'LIE', '423'),
(139, 'Lituania', 'Lithuania', 'La Lituanie', 'LT', 'LTU', '370'),
(140, 'Luxemburgo', 'Luxembourg', 'Luxembourg', 'LU', 'LUX', '352'),
(141, 'México', 'Mexico', 'Mexique', 'MX', 'MEX', '52'),
(142, 'Mónaco', 'Monaco', 'Monaco', 'MC', 'MCO', '377'),
(143, 'Macao', 'Macao', 'Macao', 'MO', 'MAC', '853'),
(144, 'Macedônia', 'Macedonia', 'Macédoine', 'MK', 'MKD', '389'),
(145, 'Madagascar', 'Madagascar', 'Madagascar', 'MG', 'MDG', '261'),
(146, 'Malasia', 'Malaysia', 'Malaisie', 'MY', 'MYS', '60'),
(147, 'Malawi', 'Malawi', 'Malawi', 'MW', 'MWI', '265'),
(148, 'Mali', 'Mali', 'Mali', 'ML', 'MLI', '223'),
(149, 'Malta', 'Malta', 'Malte', 'MT', 'MLT', '356'),
(150, 'Marruecos', 'Morocco', 'Maroc', 'MA', 'MAR', '212'),
(151, 'Martinica', 'Martinique', 'Martinique', 'MQ', 'MTQ', '596'),
(152, 'Mauricio', 'Mauritius', 'Iles Maurice', 'MU', 'MUS', '230'),
(153, 'Mauritania', 'Mauritania', 'Mauritanie', 'MR', 'MRT', '222'),
(154, 'Mayotte', 'Mayotte', 'Mayotte', 'YT', 'MYT', '262'),
(155, 'Micronesia', 'Estados Federados de', 'Federados Estados de', 'FM', 'FSM', '691'),
(156, 'Moldavia', 'Moldova', 'Moldavie', 'MD', 'MDA', '373'),
(157, 'Mongolia', 'Mongolia', 'Mongolie', 'MN', 'MNG', '976'),
(158, 'Montenegro', 'Montenegro', 'Monténégro', 'ME', 'MNE', '382'),
(159, 'Montserrat', 'Montserrat', 'Montserrat', 'MS', 'MSR', '1 664'),
(160, 'Mozambique', 'Mozambique', 'Mozambique', 'MZ', 'MOZ', '258'),
(161, 'Namibia', 'Namibia', 'Namibie', 'NA', 'NAM', '264'),
(162, 'Nauru', 'Nauru', 'Nauru', 'NR', 'NRU', '674'),
(163, 'Nepal', 'Nepal', 'Népal', 'NP', 'NPL', '977'),
(164, 'Nicaragua', 'Nicaragua', 'Nicaragua', 'NI', 'NIC', '505'),
(165, 'Niger', 'Niger', 'Niger', 'NE', 'NER', '227'),
(166, 'Nigeria', 'Nigeria', 'Nigeria', 'NG', 'NGA', '234'),
(167, 'Niue', 'Niue', 'Niou', 'NU', 'NIU', '683'),
(168, 'Noruega', 'Norway', 'Norvège', 'NO', 'NOR', '47'),
(169, 'Nueva Caledonia', 'New Caledonia', 'Nouvelle-Calédonie', 'NC', 'NCL', '687'),
(170, 'Nueva Zelanda', 'New Zealand', 'Nouvelle-Zélande', 'NZ', 'NZL', '64'),
(171, 'Omán', 'Oman', 'Oman', 'OM', 'OMN', '968'),
(172, 'Países Bajos', 'Netherlands', 'Pays-Bas', 'NL', 'NLD', '31'),
(173, 'Pakistán', 'Pakistan', 'Pakistan', 'PK', 'PAK', '92'),
(174, 'Palau', 'Palau', 'Palau', 'PW', 'PLW', '680'),
(175, 'Palestina', 'Palestine', 'La Palestine', 'PS', 'PSE', '970'),
(176, 'Panamá', 'Panama', 'Panama', 'PA', 'PAN', '507'),
(177, 'Papúa Nueva Guinea', 'Papua New Guinea', 'Papouasie-Nouvelle-Guinée', 'PG', 'PNG', '675'),
(178, 'Paraguay', 'Paraguay', 'Paraguay', 'PY', 'PRY', '595'),
(179, 'Perú', 'Peru', 'Pérou', 'PE', 'PER', '51'),
(180, 'Polinesia Francesa', 'French Polynesia', 'Polynésie française', 'PF', 'PYF', '689'),
(181, 'Polonia', 'Poland', 'Pologne', 'PL', 'POL', '48'),
(182, 'Portugal', 'Portugal', 'Portugal', 'PT', 'PRT', '351'),
(183, 'Puerto Rico', 'Puerto Rico', 'Porto Rico', 'PR', 'PRI', '1'),
(184, 'Qatar', 'Qatar', 'Qatar', 'QA', 'QAT', '974'),
(185, 'Reino Unido', 'United Kingdom', 'Royaume-Uni', 'GB', 'GBR', '44'),
(186, 'República Centroafricana', 'Central African Republic', 'République Centrafricaine', 'CF', 'CAF', '236'),
(187, 'República Checa', 'Czech Republic', 'République Tchèque', 'CZ', 'CZE', '420'),
(188, 'República Dominicana', 'Dominican Republic', 'République Dominicaine', 'DO', 'DOM', '1 809'),
(189, 'República de Sudán del Sur', 'South Sudan', 'Soudan du Sud', 'SS', 'SSD', '211'),
(190, 'Reunión', 'Réunion', 'Réunion', 'RE', 'REU', '262'),
(191, 'Ruanda', 'Rwanda', 'Rwanda', 'RW', 'RWA', '250'),
(192, 'Rumanía', 'Romania', 'Roumanie', 'RO', 'ROU', '40'),
(193, 'Rusia', 'Russia', 'La Russie', 'RU', 'RUS', '7'),
(194, 'Sahara Occidental', 'Western Sahara', 'Sahara Occidental', 'EH', 'ESH', '212'),
(195, 'Samoa', 'Samoa', 'Samoa', 'WS', 'WSM', '685'),
(196, 'Samoa Americana', 'American Samoa', 'Les Samoa américaines', 'AS', 'ASM', '1 684'),
(197, 'San Bartolomé', 'Saint Barthélemy', 'Saint-Barthélemy', 'BL', 'BLM', '590'),
(198, 'San Cristóbal y Nieves', 'Saint Kitts and Nevis', 'Saint Kitts et Nevis', 'KN', 'KNA', '1 869'),
(199, 'San Marino', 'San Marino', 'San Marino', 'SM', 'SMR', '378'),
(200, 'San Martín (Francia)', 'Saint Martin (French part)', 'Saint-Martin (partie française)', 'MF', 'MAF', '1 599'),
(201, 'San Pedro y Miquelón', 'Saint Pierre and Miquelon', 'Saint-Pierre-et-Miquelon', 'PM', 'SPM', '508'),
(202, 'San Vicente y las Granadinas', 'Saint Vincent and the Grenadines', 'Saint-Vincent et Grenadines', 'VC', 'VCT', '1 784'),
(203, 'Santa Elena', 'Ascensión y Tristán de Acuña', 'Ascensión y Tristan de Acuña', 'SH', 'SHN', '290'),
(204, 'Santa Lucía', 'Saint Lucia', 'Sainte-Lucie', 'LC', 'LCA', '1 758'),
(205, 'Santo Tomé y Príncipe', 'Sao Tome and Principe', 'Sao Tomé et Principe', 'ST', 'STP', '239'),
(206, 'Senegal', 'Senegal', 'Sénégal', 'SN', 'SEN', '221'),
(207, 'Serbia', 'Serbia', 'Serbie', 'RS', 'SRB', '381'),
(208, 'Seychelles', 'Seychelles', 'Les Seychelles', 'SC', 'SYC', '248'),
(209, 'Sierra Leona', 'Sierra Leone', 'Sierra Leone', 'SL', 'SLE', '232'),
(210, 'Singapur', 'Singapore', 'Singapour', 'SG', 'SGP', '65'),
(211, 'Sint Maarten', 'Sint Maarten', 'Saint-Martin', 'SX', 'SMX', '1 721'),
(212, 'Siria', 'Syria', 'Syrie', 'SY', 'SYR', '963'),
(213, 'Somalia', 'Somalia', 'Somalie', 'SO', 'SOM', '252'),
(214, 'Sri lanka', 'Sri Lanka', 'Sri Lanka', 'LK', 'LKA', '94'),
(215, 'Sudáfrica', 'South Africa', 'Afrique du Sud', 'ZA', 'ZAF', '27'),
(216, 'Sudán', 'Sudan', 'Soudan', 'SD', 'SDN', '249'),
(217, 'Suecia', 'Sweden', 'Suède', 'SE', 'SWE', '46'),
(218, 'Suiza', 'Switzerland', 'Suisse', 'CH', 'CHE', '41'),
(219, 'Surinám', 'Suriname', 'Surinam', 'SR', 'SUR', '597'),
(220, 'Svalbard y Jan Mayen', 'Svalbard and Jan Mayen', 'Svalbard et Jan Mayen', 'SJ', 'SJM', '47'),
(221, 'Swazilandia', 'Swaziland', 'Swaziland', 'SZ', 'SWZ', '268'),
(222, 'Tayikistán', 'Tajikistan', 'Le Tadjikistan', 'TJ', 'TJK', '992'),
(223, 'Tailandia', 'Thailand', 'Thaïlande', 'TH', 'THA', '66'),
(224, 'Taiwán', 'Taiwan', 'Taiwan', 'TW', 'TWN', '886'),
(225, 'Tanzania', 'Tanzania', 'Tanzanie', 'TZ', 'TZA', '255'),
(226, 'Territorio Británico del Océano Índico', 'British Indian Ocean Territory', 'Territoire britannique de l\'océan Indien', 'IO', 'IOT', '246'),
(227, 'Territorios Australes y Antárticas Franceses', 'French Southern Territories', 'Terres australes françaises', 'TF', 'ATF', NULL),
(228, 'Timor Oriental', 'East Timor', 'Timor-Oriental', 'TL', 'TLS', '670'),
(229, 'Togo', 'Togo', 'Togo', 'TG', 'TGO', '228'),
(230, 'Tokelau', 'Tokelau', 'Tokélaou', 'TK', 'TKL', '690'),
(231, 'Tonga', 'Tonga', 'Tonga', 'TO', 'TON', '676'),
(232, 'Trinidad y Tobago', 'Trinidad and Tobago', 'Trinidad et Tobago', 'TT', 'TTO', '1 868'),
(233, 'Tunez', 'Tunisia', 'Tunisie', 'TN', 'TUN', '216'),
(234, 'Turkmenistán', 'Turkmenistan', 'Le Turkménistan', 'TM', 'TKM', '993'),
(235, 'Turquía', 'Turkey', 'Turquie', 'TR', 'TUR', '90'),
(236, 'Tuvalu', 'Tuvalu', 'Tuvalu', 'TV', 'TUV', '688'),
(237, 'Ucrania', 'Ukraine', 'L\'Ukraine', 'UA', 'UKR', '380'),
(238, 'Uganda', 'Uganda', 'Ouganda', 'UG', 'UGA', '256'),
(239, 'Uruguay', 'Uruguay', 'Uruguay', 'UY', 'URY', '598'),
(240, 'Uzbekistán', 'Uzbekistan', 'L\'Ouzbékistan', 'UZ', 'UZB', '998'),
(241, 'Vanuatu', 'Vanuatu', 'Vanuatu', 'VU', 'VUT', '678'),
(242, 'Venezuela', 'Venezuela', 'Venezuela', 'VE', 'VEN', '58'),
(243, 'Vietnam', 'Vietnam', 'Vietnam', 'VN', 'VNM', '84'),
(244, 'Wallis y Futuna', 'Wallis and Futuna', 'Wallis et Futuna', 'WF', 'WLF', '681'),
(245, 'Yemen', 'Yemen', 'Yémen', 'YE', 'YEM', '967'),
(246, 'Yibuti', 'Djibouti', 'Djibouti', 'DJ', 'DJI', '253'),
(247, 'Zambia', 'Zambia', 'Zambie', 'ZM', 'ZMB', '260'),
(248, 'Zimbabue', 'Zimbabwe', 'Zimbabwe', 'ZW', 'ZWE', '263');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `propabilidad`
--

CREATE TABLE `propabilidad` (
  `propabilidad_id` int(11) NOT NULL,
  `propabilidad_categoria` varchar(70) NOT NULL,
  `propabilidad_valor` int(11) NOT NULL,
  `proyecto_id` int(11) NOT NULL,
  `proyecto_linea_base` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proyecto`
--

CREATE TABLE `proyecto` (
  `proyecto_id` int(11) NOT NULL,
  `proyecto_nombre` varchar(100) NOT NULL,
  `proyecto_objetivo` text DEFAULT NULL,
  `proyecto_alcance` text DEFAULT NULL,
  `proyecto_descripcion` text DEFAULT NULL,
  `proyecto_presupuesto` float DEFAULT NULL,
  `proyecto_fecha_inicio` date DEFAULT NULL,
  `proyecto_fecha_finl` date DEFAULT NULL,
  `proyecto_evaluacion_general` text DEFAULT NULL,
  `proyecto_evaluacion` int(11) DEFAULT NULL,
  `proyecto_rbs_status` tinyint(4) NOT NULL DEFAULT 0,
  `proyecto_fin_status` tinyint(4) NOT NULL DEFAULT 0,
  `proyecto_fecha_linea_base` datetime DEFAULT current_timestamp(),
  `gerente_id` int(11) NOT NULL,
  `sector_id` int(11) NOT NULL,
  `proyecto_linea_base` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proyecto_has_riesgo`
--

CREATE TABLE `proyecto_has_riesgo` (
  `proyecto_has_riesgo_id` int(11) NOT NULL,
  `riesgo_id` int(11) NOT NULL,
  `is_editado` int(11) NOT NULL DEFAULT 0,
  `impacto_id` int(11) DEFAULT NULL,
  `propabilidad_id` int(11) DEFAULT NULL,
  `fecha_manifestacion` datetime DEFAULT NULL,
  `proyecto_id` int(11) NOT NULL,
  `responsable_id` int(11) DEFAULT NULL,
  `proyecto_linea_base` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proyecto_has_riesgo_actividad`
--

CREATE TABLE `proyecto_has_riesgo_actividad` (
  `proyecto_has_riesgo_actividad_id` int(11) NOT NULL,
  `actividad_id` varchar(45) NOT NULL,
  `proyecto_has_riesgo_id` int(11) NOT NULL,
  `proyecto_linea_base` int(11) NOT NULL,
  `proyecto_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proyecto_has_riesgo_respuesta`
--

CREATE TABLE `proyecto_has_riesgo_respuesta` (
  `proyecto_has_id` int(11) NOT NULL,
  `respuesta_has_id` int(11) NOT NULL,
  `tipo_respuesta` varchar(30) NOT NULL,
  `proyecto_linea_base` int(11) NOT NULL,
  `proyecto_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rbs`
--

CREATE TABLE `rbs` (
  `rbs_id` int(11) NOT NULL,
  `rbs_default` tinyint(4) NOT NULL DEFAULT 0 COMMENT 'Permite saber si se eligio la rbs por defecto del pmbok o se decidio por otra opcion.',
  `gerente_id` int(11) NOT NULL,
  `proyecto_linea_base` int(11) NOT NULL,
  `proyecto_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `recurso`
--

CREATE TABLE `recurso` (
  `recurso_id` int(11) NOT NULL,
  `recurso_nombre` varchar(45) DEFAULT NULL,
  `recurso_costo` float DEFAULT 0,
  `tipo_recurso_id` int(11) NOT NULL,
  `proyecto_id` int(11) NOT NULL,
  `proyecto_linea_base` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `responsble`
--

CREATE TABLE `responsble` (
  `responsable_id` int(11) NOT NULL,
  `responsble_nombre` varchar(100) NOT NULL,
  `responsble_descripcion` text DEFAULT NULL,
  `rol_id` int(11) NOT NULL,
  `proyecto_id` int(11) NOT NULL,
  `proyecto_linea_base` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `respuesta`
--

CREATE TABLE `respuesta` (
  `respuesta_id` int(11) NOT NULL,
  `respuesta_nombre` varchar(45) DEFAULT NULL,
  `respuesta_tipo` varchar(30) NOT NULL,
  `respuesta_descripcion` text DEFAULT NULL,
  `respuesta_costo` float DEFAULT 0,
  `proyecto_linea_base` int(11) NOT NULL,
  `proyecto_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `riesgo`
--

CREATE TABLE `riesgo` (
  `riesgo_id` int(11) NOT NULL,
  `proyecto_linea_base` int(11) NOT NULL,
  `riesgo_nombre` varchar(45) DEFAULT NULL,
  `riesgo_causa` text DEFAULT NULL,
  `riesgo_evento` text DEFAULT NULL,
  `riesgo_efecto` text DEFAULT NULL,
  `riesgo_tipo` tinyint(4) DEFAULT NULL COMMENT '0 si es un riesgo, 1 si es oportunidad',
  `riesgo_prom_evaluacion` float DEFAULT 0 COMMENT 'La evaluacion del riesgo de acuerdo a todos los proyectos.',
  `riesgo_uid` bigint(20) UNSIGNED DEFAULT NULL,
  `sub_categoria_id` int(11) NOT NULL,
  `proyecto_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `riesgo_has_respuesta`
--

CREATE TABLE `riesgo_has_respuesta` (
  `riesgo_has_respuesta_id` int(11) NOT NULL,
  `riesgo_id` int(11) NOT NULL,
  `respuesta_id` int(11) NOT NULL,
  `proyecto_linea_base` int(11) NOT NULL,
  `proyecto_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol`
--

CREATE TABLE `rol` (
  `rol_id` int(11) NOT NULL,
  `rol_nombre` varchar(60) NOT NULL,
  `rol_descripcion` text DEFAULT NULL,
  `gerente_id` int(11) NOT NULL,
  `proyecto_linea_base` int(11) NOT NULL,
  `proyecto_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sector`
--

CREATE TABLE `sector` (
  `sector_id` int(11) NOT NULL,
  `sector_nombre` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


INSERT INTO `sector` (`sector_id`, `sector_nombre`) VALUES
(9, 'agropecuario'),
(10, 'servicios'),
(11, 'transporte'),
(12, 'comercio'),
(13, 'financiero'),
(14, 'construcción'),
(15, 'minero'),
(16, 'comunicaciones'),
(17, 'educación'),
(18, 'gobierno');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sub_categoria`
--

CREATE TABLE `sub_categoria` (
  `sub_categoria_id` int(11) NOT NULL,
  `sub_categoria_nombre` varchar(45) DEFAULT NULL,
  `sub_categoria_descripcion` text DEFAULT NULL,
  `sub_categoria_default` tinyint(4) NOT NULL DEFAULT 1,
  `sub_categoria_uid` bigint(20) UNSIGNED DEFAULT NULL,
  `sub_categoria_linea_base` int(11) DEFAULT 0,
  `categoria_id` int(11) NOT NULL,
  `proyecto_linea_base` int(11) NOT NULL,
  `proyecto_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tarea`
--

CREATE TABLE `tarea` (
  `tarea_id` int(11) NOT NULL,
  `proyecto_linea_base` int(11) NOT NULL,
  `tarea_nombre` varchar(77) NOT NULL,
  `tarea_descripcion` text NOT NULL,
  `proyecto_has_riesgo_id` int(11) NOT NULL,
  `riesgo_has_respuesta_id` int(11) NOT NULL,
  `fecha_inicio` datetime DEFAULT NULL,
  `duracion` int(11) DEFAULT NULL,
  `fecha_fin` datetime DEFAULT NULL,
  `fecha_inicio_real` datetime DEFAULT NULL,
  `duracion_real` int(11) DEFAULT NULL,
  `fecha_fin_real` datetime DEFAULT NULL,
  `tarea_observacion` text DEFAULT '',
  `tarea_estado` tinyint(4) DEFAULT NULL COMMENT '1) No inciado (cuando se registra y nunca le pone fecha de inicio real)\n2) Iniciado (Registra una fecha de inicio real)\n3) Completado (Cuando usted registra una fecha de fin real)\n4) Retrasado (Cuando esta iniciada y la fecha de fin planeada se paso)',
  `proyecto_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tarea_has_recurso`
--

CREATE TABLE `tarea_has_recurso` (
  `tarea_id` int(11) NOT NULL,
  `recurso_id` int(11) NOT NULL,
  `proyecto_linea_base` int(11) NOT NULL,
  `cantidad` float NOT NULL,
  `proyecto_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_recurso`
--

CREATE TABLE `tipo_recurso` (
  `tipo_recurso_id` int(11) NOT NULL,
  `proyecto_linea_base` int(11) NOT NULL,
  `tipo_recurso_nombre` varchar(45) NOT NULL,
  `tipo_recurso_descripcion` text DEFAULT NULL,
  `gerente_id` int(11) NOT NULL,
  `proyecto_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `actividad`
--
ALTER TABLE `actividad`
  ADD PRIMARY KEY (`actividad_id`,`proyecto_linea_base`,`proyecto_id`),
  ADD KEY `fk_actividad_proyecto1_idx` (`proyecto_id`,`proyecto_linea_base`);

--
-- Indices de la tabla `categoria`
--
ALTER TABLE `categoria`
  ADD PRIMARY KEY (`categoria_id`,`proyecto_linea_base`,`proyecto_id`),
  ADD KEY `fk_categoria_rbs1_idx` (`rbs_id`,`proyecto_linea_base`,`proyecto_id`);

--
-- Indices de la tabla `clasificacion_riesgo`
--
ALTER TABLE `clasificacion_riesgo`
  ADD PRIMARY KEY (`clasificacion_riesgo_id`,`proyecto_linea_base`,`proyecto_id`),
  ADD KEY `fk_clasificacion_riesgo_proyecto1_idx` (`proyecto_id`,`proyecto_linea_base`);

--
-- Indices de la tabla `gerente`
--
ALTER TABLE `gerente`
  ADD PRIMARY KEY (`gerente_id`,`proyecto_linea_base`,`proyecto_id`),
  ADD KEY `fk_gerente_sector1_idx` (`sector_id`),
  ADD KEY `fk_gerente_pais1_idx` (`pais_id`);

--
-- Indices de la tabla `impacto`
--
ALTER TABLE `impacto`
  ADD PRIMARY KEY (`impacto_id`,`proyecto_linea_base`,`proyecto_id`),
  ADD KEY `fk_impacto_proyecto1_idx` (`proyecto_id`,`proyecto_linea_base`);

--
-- Indices de la tabla `leccion`
--
ALTER TABLE `leccion`
  ADD PRIMARY KEY (`leccion_id`),
  ADD KEY `fk_leccion_proyecto_idx` (`proyecto_id`,`proyecto_linea_base`);

--
-- Indices de la tabla `pais`
--
ALTER TABLE `pais`
  ADD PRIMARY KEY (`pais_id`);

--
-- Indices de la tabla `propabilidad`
--
ALTER TABLE `propabilidad`
  ADD PRIMARY KEY (`propabilidad_id`,`proyecto_linea_base`,`proyecto_id`),
  ADD KEY `fk_propabilidad_proyecto1_idx` (`proyecto_id`,`proyecto_linea_base`);

--
-- Indices de la tabla `proyecto`
--
ALTER TABLE `proyecto`
  ADD PRIMARY KEY (`proyecto_id`,`proyecto_linea_base`),
  ADD KEY `fk_proyecto_gerente1_idx` (`gerente_id`,`proyecto_linea_base`),
  ADD KEY `fk_proyecto_sector1_idx` (`sector_id`);

--
-- Indices de la tabla `proyecto_has_riesgo`
--
ALTER TABLE `proyecto_has_riesgo`
  ADD PRIMARY KEY (`proyecto_has_riesgo_id`,`proyecto_linea_base`,`proyecto_id`),
  ADD KEY `fk_proyecto_has_riesgo_proyecto1_idx` (`proyecto_id`,`proyecto_linea_base`),
  ADD KEY `fk_proyecto_has_riesgo_responsble1_idx` (`responsable_id`,`proyecto_linea_base`,`proyecto_id`),
  ADD KEY `fk_proyecto_has_riesgo_propabilidad1_idx` (`propabilidad_id`,`proyecto_linea_base`,`proyecto_id`),
  ADD KEY `fk_proyecto_has_riesgo_impacto1_idx` (`impacto_id`,`proyecto_linea_base`,`proyecto_id`),
  ADD KEY `fk_proyecto_has_riesgo_riesgo1_idx` (`riesgo_id`,`proyecto_linea_base`,`proyecto_id`);

--
-- Indices de la tabla `proyecto_has_riesgo_actividad`
--
ALTER TABLE `proyecto_has_riesgo_actividad`
  ADD PRIMARY KEY (`proyecto_has_riesgo_actividad_id`,`proyecto_linea_base`,`proyecto_id`),
  ADD KEY `fk_proyecto_has_riesgo_actividad_actividad1_idx` (`actividad_id`,`proyecto_linea_base`,`proyecto_id`),
  ADD KEY `fk_proyecto_has_riesgo_actividad_proyecto_has_riesgo1_idx` (`proyecto_has_riesgo_id`,`proyecto_linea_base`,`proyecto_id`);

--
-- Indices de la tabla `proyecto_has_riesgo_respuesta`
--
ALTER TABLE `proyecto_has_riesgo_respuesta`
  ADD PRIMARY KEY (`proyecto_has_id`,`respuesta_has_id`,`proyecto_linea_base`,`proyecto_id`),
  ADD KEY `fk_proyecto_has_riesgo_respuesta_riesgo_has_respuesta1_idx` (`respuesta_has_id`,`proyecto_linea_base`,`proyecto_id`),
  ADD KEY `fk_proyecto_has_riesgo_respuesta_proyecto_has_riesgo1_idx` (`proyecto_has_id`,`proyecto_linea_base`,`proyecto_id`);

--
-- Indices de la tabla `rbs`
--
ALTER TABLE `rbs`
  ADD PRIMARY KEY (`rbs_id`,`proyecto_linea_base`,`proyecto_id`),
  ADD KEY `fk_rbs_gerente1_idx` (`gerente_id`,`proyecto_linea_base`,`proyecto_id`);

--
-- Indices de la tabla `recurso`
--
ALTER TABLE `recurso`
  ADD PRIMARY KEY (`recurso_id`,`proyecto_linea_base`,`proyecto_id`),
  ADD KEY `fk_recurso_proyecto1_idx` (`proyecto_id`,`proyecto_linea_base`),
  ADD KEY `fk_recurso_tipo_recurso1_idx` (`tipo_recurso_id`,`proyecto_linea_base`,`proyecto_id`);

--
-- Indices de la tabla `responsble`
--
ALTER TABLE `responsble`
  ADD PRIMARY KEY (`responsable_id`,`proyecto_linea_base`,`proyecto_id`),
  ADD KEY `fk_responsble_proyecto1_idx` (`proyecto_id`,`proyecto_linea_base`),
  ADD KEY `fk_responsble_rol1_idx` (`rol_id`,`proyecto_linea_base`,`proyecto_id`);

--
-- Indices de la tabla `respuesta`
--
ALTER TABLE `respuesta`
  ADD PRIMARY KEY (`respuesta_id`,`proyecto_linea_base`,`proyecto_id`);

--
-- Indices de la tabla `riesgo`
--
ALTER TABLE `riesgo`
  ADD PRIMARY KEY (`riesgo_id`,`proyecto_linea_base`,`proyecto_id`),
  ADD KEY `fk_riesgo_sub_categoria1_idx` (`sub_categoria_id`,`proyecto_linea_base`,`proyecto_id`);

--
-- Indices de la tabla `riesgo_has_respuesta`
--
ALTER TABLE `riesgo_has_respuesta`
  ADD PRIMARY KEY (`riesgo_has_respuesta_id`,`proyecto_linea_base`,`proyecto_id`),
  ADD KEY `fk_riesgo_has_respuesta_respuesta1_idx` (`respuesta_id`,`proyecto_linea_base`,`proyecto_id`),
  ADD KEY `fk_riesgo_has_respuesta_riesgo1_idx` (`riesgo_id`,`proyecto_linea_base`,`proyecto_id`);

--
-- Indices de la tabla `rol`
--
ALTER TABLE `rol`
  ADD PRIMARY KEY (`rol_id`,`proyecto_linea_base`,`proyecto_id`),
  ADD KEY `fk_rol_gerente1_idx` (`gerente_id`,`proyecto_linea_base`,`proyecto_id`);

--
-- Indices de la tabla `sector`
--
ALTER TABLE `sector`
  ADD PRIMARY KEY (`sector_id`);

--
-- Indices de la tabla `sub_categoria`
--
ALTER TABLE `sub_categoria`
  ADD PRIMARY KEY (`sub_categoria_id`,`proyecto_linea_base`,`proyecto_id`),
  ADD KEY `fk_sub_categoria_categoria1_idx` (`categoria_id`,`proyecto_linea_base`,`proyecto_id`);

--
-- Indices de la tabla `tarea`
--
ALTER TABLE `tarea`
  ADD PRIMARY KEY (`tarea_id`,`proyecto_linea_base`,`proyecto_id`),
  ADD KEY `fk_proyecto_has_riesgo_respuesta_idx` (`proyecto_has_riesgo_id`,`riesgo_has_respuesta_id`,`proyecto_linea_base`,`proyecto_id`);

--
-- Indices de la tabla `tarea_has_recurso`
--
ALTER TABLE `tarea_has_recurso`
  ADD PRIMARY KEY (`tarea_id`,`recurso_id`,`proyecto_linea_base`,`proyecto_id`),
  ADD KEY `fk_tarea_has_recurso_recurso1_idx` (`recurso_id`,`proyecto_linea_base`,`proyecto_id`),
  ADD KEY `fk_tarea_has_recurso_tarea1_idx` (`tarea_id`,`proyecto_linea_base`,`proyecto_id`);

--
-- Indices de la tabla `tipo_recurso`
--
ALTER TABLE `tipo_recurso`
  ADD PRIMARY KEY (`tipo_recurso_id`,`proyecto_linea_base`,`proyecto_id`),
  ADD KEY `fk_tipo_recurso_gerente1_idx` (`gerente_id`,`proyecto_linea_base`,`proyecto_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `categoria`
--
ALTER TABLE `categoria`
  MODIFY `categoria_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `clasificacion_riesgo`
--
ALTER TABLE `clasificacion_riesgo`
  MODIFY `clasificacion_riesgo_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `gerente`
--
ALTER TABLE `gerente`
  MODIFY `gerente_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `impacto`
--
ALTER TABLE `impacto`
  MODIFY `impacto_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `leccion`
--
ALTER TABLE `leccion`
  MODIFY `leccion_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `pais`
--
ALTER TABLE `pais`
  MODIFY `pais_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `propabilidad`
--
ALTER TABLE `propabilidad`
  MODIFY `propabilidad_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `proyecto`
--
ALTER TABLE `proyecto`
  MODIFY `proyecto_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `proyecto_has_riesgo`
--
ALTER TABLE `proyecto_has_riesgo`
  MODIFY `proyecto_has_riesgo_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `proyecto_has_riesgo_actividad`
--
ALTER TABLE `proyecto_has_riesgo_actividad`
  MODIFY `proyecto_has_riesgo_actividad_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `rbs`
--
ALTER TABLE `rbs`
  MODIFY `rbs_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `recurso`
--
ALTER TABLE `recurso`
  MODIFY `recurso_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `responsble`
--
ALTER TABLE `responsble`
  MODIFY `responsable_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `respuesta`
--
ALTER TABLE `respuesta`
  MODIFY `respuesta_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `riesgo`
--
ALTER TABLE `riesgo`
  MODIFY `riesgo_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `riesgo_has_respuesta`
--
ALTER TABLE `riesgo_has_respuesta`
  MODIFY `riesgo_has_respuesta_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `rol`
--
ALTER TABLE `rol`
  MODIFY `rol_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `sector`
--
ALTER TABLE `sector`
  MODIFY `sector_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `sub_categoria`
--
ALTER TABLE `sub_categoria`
  MODIFY `sub_categoria_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tarea`
--
ALTER TABLE `tarea`
  MODIFY `tarea_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tipo_recurso`
--
ALTER TABLE `tipo_recurso`
  MODIFY `tipo_recurso_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `actividad`
--
ALTER TABLE `actividad`
  ADD CONSTRAINT `fk_actividad_proyecto1` FOREIGN KEY (`proyecto_id`,`proyecto_linea_base`) REFERENCES `proyecto` (`proyecto_id`, `proyecto_linea_base`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `categoria`
--
ALTER TABLE `categoria`
  ADD CONSTRAINT `fk_categoria_rbs1` FOREIGN KEY (`rbs_id`,`proyecto_linea_base`,`proyecto_id`) REFERENCES `rbs` (`rbs_id`, `proyecto_linea_base`, `proyecto_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `clasificacion_riesgo`
--
ALTER TABLE `clasificacion_riesgo`
  ADD CONSTRAINT `fk_clasificacion_riesgo_proyecto1` FOREIGN KEY (`proyecto_id`,`proyecto_linea_base`) REFERENCES `proyecto` (`proyecto_id`, `proyecto_linea_base`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `gerente`
--
ALTER TABLE `gerente`
  ADD CONSTRAINT `fk_gerente_pais1` FOREIGN KEY (`pais_id`) REFERENCES `pais` (`pais_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_gerente_sector1` FOREIGN KEY (`sector_id`) REFERENCES `sector` (`sector_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `impacto`
--
ALTER TABLE `impacto`
  ADD CONSTRAINT `fk_impacto_proyecto1` FOREIGN KEY (`proyecto_id`,`proyecto_linea_base`) REFERENCES `proyecto` (`proyecto_id`, `proyecto_linea_base`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `leccion`
--
ALTER TABLE `leccion`
  ADD CONSTRAINT `fk_leccion_proyecto` FOREIGN KEY (`proyecto_id`,`proyecto_linea_base`) REFERENCES `proyecto` (`proyecto_id`, `proyecto_linea_base`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `propabilidad`
--
ALTER TABLE `propabilidad`
  ADD CONSTRAINT `fk_propabilidad_proyecto1` FOREIGN KEY (`proyecto_id`,`proyecto_linea_base`) REFERENCES `proyecto` (`proyecto_id`, `proyecto_linea_base`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `proyecto`
--
ALTER TABLE `proyecto`
  ADD CONSTRAINT `fk_proyecto_gerente1` FOREIGN KEY (`gerente_id`,`proyecto_linea_base`) REFERENCES `gerente` (`gerente_id`, `proyecto_linea_base`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_proyecto_sector1` FOREIGN KEY (`sector_id`) REFERENCES `sector` (`sector_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `proyecto_has_riesgo`
--
ALTER TABLE `proyecto_has_riesgo`
  ADD CONSTRAINT `fk_proyecto_has_riesgo_impacto1` FOREIGN KEY (`impacto_id`,`proyecto_linea_base`,`proyecto_id`) REFERENCES `impacto` (`impacto_id`, `proyecto_linea_base`, `proyecto_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_proyecto_has_riesgo_propabilidad1` FOREIGN KEY (`propabilidad_id`,`proyecto_linea_base`,`proyecto_id`) REFERENCES `propabilidad` (`propabilidad_id`, `proyecto_linea_base`, `proyecto_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_proyecto_has_riesgo_proyecto1` FOREIGN KEY (`proyecto_id`,`proyecto_linea_base`) REFERENCES `proyecto` (`proyecto_id`, `proyecto_linea_base`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_proyecto_has_riesgo_responsble1` FOREIGN KEY (`responsable_id`,`proyecto_linea_base`,`proyecto_id`) REFERENCES `responsble` (`responsable_id`, `proyecto_linea_base`, `proyecto_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_proyecto_has_riesgo_riesgo1` FOREIGN KEY (`riesgo_id`,`proyecto_linea_base`,`proyecto_id`) REFERENCES `riesgo` (`riesgo_id`, `proyecto_linea_base`, `proyecto_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `proyecto_has_riesgo_actividad`
--
ALTER TABLE `proyecto_has_riesgo_actividad`
  ADD CONSTRAINT `fk_proyecto_has_riesgo_actividad_actividad1` FOREIGN KEY (`actividad_id`,`proyecto_linea_base`,`proyecto_id`) REFERENCES `actividad` (`actividad_id`, `proyecto_linea_base`, `proyecto_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_proyecto_has_riesgo_actividad_proyecto_has_riesgo1` FOREIGN KEY (`proyecto_has_riesgo_id`,`proyecto_linea_base`,`proyecto_id`) REFERENCES `proyecto_has_riesgo` (`proyecto_has_riesgo_id`, `proyecto_linea_base`, `proyecto_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `proyecto_has_riesgo_respuesta`
--
ALTER TABLE `proyecto_has_riesgo_respuesta`
  ADD CONSTRAINT `fk_proyecto_has_riesgo_respuesta_proyecto_has_riesgo1` FOREIGN KEY (`proyecto_has_id`,`proyecto_linea_base`,`proyecto_id`) REFERENCES `proyecto_has_riesgo` (`proyecto_has_riesgo_id`, `proyecto_linea_base`, `proyecto_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_proyecto_has_riesgo_respuesta_riesgo_has_respuesta1` FOREIGN KEY (`respuesta_has_id`,`proyecto_linea_base`,`proyecto_id`) REFERENCES `riesgo_has_respuesta` (`riesgo_has_respuesta_id`, `proyecto_linea_base`, `proyecto_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `rbs`
--
ALTER TABLE `rbs`
  ADD CONSTRAINT `fk_rbs_gerente1` FOREIGN KEY (`gerente_id`,`proyecto_linea_base`,`proyecto_id`) REFERENCES `gerente` (`gerente_id`, `proyecto_linea_base`, `proyecto_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `recurso`
--
ALTER TABLE `recurso`
  ADD CONSTRAINT `fk_recurso_proyecto1` FOREIGN KEY (`proyecto_id`,`proyecto_linea_base`) REFERENCES `proyecto` (`proyecto_id`, `proyecto_linea_base`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_recurso_tipo_recurso1` FOREIGN KEY (`tipo_recurso_id`,`proyecto_linea_base`,`proyecto_id`) REFERENCES `tipo_recurso` (`tipo_recurso_id`, `proyecto_linea_base`, `proyecto_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `responsble`
--
ALTER TABLE `responsble`
  ADD CONSTRAINT `fk_responsble_proyecto1` FOREIGN KEY (`proyecto_id`,`proyecto_linea_base`) REFERENCES `proyecto` (`proyecto_id`, `proyecto_linea_base`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_responsble_rol1` FOREIGN KEY (`rol_id`,`proyecto_linea_base`,`proyecto_id`) REFERENCES `rol` (`rol_id`, `proyecto_linea_base`, `proyecto_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `riesgo`
--
ALTER TABLE `riesgo`
  ADD CONSTRAINT `fk_riesgo_sub_categoria1` FOREIGN KEY (`sub_categoria_id`,`proyecto_linea_base`,`proyecto_id`) REFERENCES `sub_categoria` (`sub_categoria_id`, `proyecto_linea_base`, `proyecto_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `riesgo_has_respuesta`
--
ALTER TABLE `riesgo_has_respuesta`
  ADD CONSTRAINT `fk_riesgo_has_respuesta_respuesta1` FOREIGN KEY (`respuesta_id`,`proyecto_linea_base`,`proyecto_id`) REFERENCES `respuesta` (`respuesta_id`, `proyecto_linea_base`, `proyecto_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_riesgo_has_respuesta_riesgo1` FOREIGN KEY (`riesgo_id`,`proyecto_linea_base`,`proyecto_id`) REFERENCES `riesgo` (`riesgo_id`, `proyecto_linea_base`, `proyecto_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `rol`
--
ALTER TABLE `rol`
  ADD CONSTRAINT `fk_rol_gerente1` FOREIGN KEY (`gerente_id`,`proyecto_linea_base`,`proyecto_id`) REFERENCES `gerente` (`gerente_id`, `proyecto_linea_base`, `proyecto_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `sub_categoria`
--
ALTER TABLE `sub_categoria`
  ADD CONSTRAINT `fk_sub_categoria_categoria1` FOREIGN KEY (`categoria_id`,`proyecto_linea_base`,`proyecto_id`) REFERENCES `categoria` (`categoria_id`, `proyecto_linea_base`, `proyecto_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `tarea`
--
ALTER TABLE `tarea`
  ADD CONSTRAINT `fk_proyecto_has_riesgo_respuesta` FOREIGN KEY (`proyecto_has_riesgo_id`,`riesgo_has_respuesta_id`,`proyecto_linea_base`,`proyecto_id`) REFERENCES `proyecto_has_riesgo_respuesta` (`proyecto_has_id`, `respuesta_has_id`, `proyecto_linea_base`, `proyecto_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `tarea_has_recurso`
--
ALTER TABLE `tarea_has_recurso`
  ADD CONSTRAINT `fk_tarea_has_recurso_recurso1` FOREIGN KEY (`recurso_id`,`proyecto_linea_base`,`proyecto_id`) REFERENCES `recurso` (`recurso_id`, `proyecto_linea_base`, `proyecto_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_tarea_has_recurso_tarea1` FOREIGN KEY (`tarea_id`,`proyecto_linea_base`,`proyecto_id`) REFERENCES `tarea` (`tarea_id`, `proyecto_linea_base`, `proyecto_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `tipo_recurso`
--
ALTER TABLE `tipo_recurso`
  ADD CONSTRAINT `fk_tipo_recurso_gerente1` FOREIGN KEY (`gerente_id`,`proyecto_linea_base`,`proyecto_id`) REFERENCES `gerente` (`gerente_id`, `proyecto_linea_base`, `proyecto_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
