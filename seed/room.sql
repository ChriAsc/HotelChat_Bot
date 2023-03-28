-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Creato il: Mar 28, 2023 alle 11:01
-- Versione del server: 10.4.24-MariaDB
-- Versione PHP: 7.4.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_rasa_cb`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `room`
--

CREATE TABLE `room` (
  `room_id` int(11) NOT NULL,
  `room_type` text NOT NULL,
  `reservations` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dump dei dati per la tabella `room`
--

INSERT INTO `room` (`room_id`, `room_type`, `reservations`) VALUES
(1, 'Standard', '{\n   \"res\": [\n      {\n         \"check_in\": \"06/12/2023\",\n         \"check_out\": \"10/12/2023\",\n         \"reference\": \"Christian Ascani\"\n      },\n      {\n         \"check_in\": \"21/12/2023\",\n         \"check_out\": \"27/12/2023\",\n         \"reference\": \"Paolo Rossi\"\n      },\n      {\n         \"check_in\": \"30/12/2023\",\n         \"check_out\": \"03/01/2024\",\n         \"reference\": \"Alessandro Bedetta\"\n      }\n   ]\n}'),
(2, 'Deluxe', '{\n  \"res\": [\n    {\n      \"check_in\": \"21/07/2023\",\n      \"check_out\": \"30/07/2023\",\n      \"reference\": \"Giovanni Rana\"\n    },\n    {\n      \"check_in\": \"13/08/2023\",\n      \"check_out\": \"21/08/2023\",\n      \"reference\": \"Gino Paoli\"\n    },\n    {\n      \"check_in\": \"05/09/2024\",\n      \"check_out\": \"12/09/2024\",\n      \"reference\": \"John Doe\"\n    }\n  ]\n}'),
(3, 'Presidential', '{   \n  \"res\": [\n    {\n      \"check_in\": \"15/07/2023\",\n      \"check_out\": \"24/07/2023\",\n      \"reference\": \"Sandro Tonali\"\n    },\n    {\n      \"check_in\": \"20/12/2023\", \n      \"check_out\": \"06/01/2024\",\n      \"reference\": \"Stefano Pioli\"\n    },\n    {\n      \"check_in\": \"13/02/2024\",\n      \"check_out\": \"24/02/2024\",\n      \"reference\": \"Jerry Calà\"\n    }\n  ]\n}'),
(4, 'Standard', '{\n   \"res\": [\n     {\n         \"check_in\":\"10/08/2023\",\n         \"check_out\":\"20/08/2023\",\n         \"reference\":\"Gianluca Busani\"\n     },\n     {\n         \"check_in\":\"24/12/2023\",\n         \"check_out\":\"07/01/2024\",\n         \"reference\":\"Vittorio Sgarbi\"\n     },\n     {\n         \"check_in\":\"12/01/2024\",\n         \"check_out\":\"20/01/2024\",\n         \"reference\":\"Vittorio Feltri\"\n     }\n   ]\n}'),
(5, 'Standard', '{\n  \"res\": [\n    {\n      \"check_in\": \"02/04/2023\",\n      \"check_out\": \"11/04/2023\",\n      \"reference\": \"Pierpaolo Pasolini\"\n    },\n    {\n      \"check_in\": \"13/05/2023\",\n      \"check_out\": \"26/05/2023\",\n      \"reference\": \"Giordano Mario\"\n    },\n    {\n      \"check_in\": \"30/06/2023\",\n      \"check_out\": \"06/07/2023\",\n      \"reference\": \"David Parenzo\"\n    },\n    {\n      \"check_in\": \"30/10/2023\",\n      \"check_out\": \"11/11/2023\",\n      \"reference\": \"Giuseppe Cruciani\"\n    }\n  ]\n}'),
(6, 'Deluxe', '{\n  \"res\": [\n    {\n      \"check_in\": \"09/02/2024\",\n      \"check_out\": \"15/12/2024\",\n      \"reference\": \"Simone Amatucci\"\n    },\n    {\n      \"check_in\": \"11/03/2024\",\n      \"check_out\": \"19/03/2024\",\n      \"reference\": \"Elio Teso\"\n    },\n    {\n      \"check_in\": \"27/11/2024\",\n      \"check_out\": \"02/12/2024\",\n      \"reference\": \"Gianluca Spalazzi\"\n    }\n  ]\n}');

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `room`
--
ALTER TABLE `room`
  ADD PRIMARY KEY (`room_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
