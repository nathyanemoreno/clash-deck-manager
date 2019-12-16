-- MySQL Script generated by MySQL Workbench
-- sáb 14 dez 2019 22:49:55 -03
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema CLASHROYALE
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `CLASHROYALE` ;

-- -----------------------------------------------------
-- Schema CLASHROYALE
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `CLASHROYALE` DEFAULT CHARACTER SET latin1 ;
USE `CLASHROYALE` ;

-- -----------------------------------------------------
-- Table `CLASHROYALE`.`cartas`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `CLASHROYALE`.`cartas` ;

CREATE TABLE IF NOT EXISTS `CLASHROYALE`.`cartas` (
  `numero_carta` INT(11) NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(50) NOT NULL,
  `raridade` VARCHAR(50) NOT NULL,
  `custo` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`numero_carta`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `CLASHROYALE`.`decks`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `CLASHROYALE`.`decks` ;

CREATE TABLE IF NOT EXISTS `CLASHROYALE`.`decks` (
  `codigo_deck` INT(11) NOT NULL AUTO_INCREMENT,
  `descricao` VARCHAR(200) NULL DEFAULT NULL,
  `nome` VARCHAR(50) NOT NULL,
  `custo` DECIMAL(2,1) NULL DEFAULT NULL,
  `data_criacao` DATE NULL DEFAULT NULL,
  PRIMARY KEY (`codigo_deck`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `CLASHROYALE`.`deck_cartas`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `CLASHROYALE`.`deck_cartas` ;

CREATE TABLE IF NOT EXISTS `CLASHROYALE`.`deck_cartas` (
  `codigo_deck` INT(11) NOT NULL,
  `numero_carta` INT(11) NOT NULL,
  `index_carta` INT(11) NOT NULL,
  PRIMARY KEY (`codigo_deck`, `index_carta`),
  INDEX `numero_carta` (`numero_carta` ASC),
  CONSTRAINT `DECK_cartas_ibfk_1`
    FOREIGN KEY (`codigo_deck`)
    REFERENCES `CLASHROYALE`.`decks` (`codigo_deck`),
  CONSTRAINT `DECK_cartas_ibfk_2`
    FOREIGN KEY (`numero_carta`)
    REFERENCES `CLASHROYALE`.`cartas` (`numero_carta`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
