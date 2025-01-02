CREATE DATABASE  IF NOT EXISTS `negocioimportaciones` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `negocioimportaciones`;
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: negocioimportaciones
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cliente`
--

DROP TABLE IF EXISTS `cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente` (
  `idCliente` int NOT NULL,
  `nombreCompleto` char(50) NOT NULL,
  `cedula` char(10) NOT NULL,
  `dirreccion` char(50) NOT NULL,
  PRIMARY KEY (`idCliente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
INSERT INTO `cliente` VALUES (1,'Juan Morales','0993761846','Av Junin 200 y Panama'),(2,'Sergio Ramírez','0993618492','9 de octubre'),(3,'Lucía Pérez','0994789107','Utb La Joya etapa Platino mz 18 v 10'),(4,'Marta Gómez','0946351627','Calle 1'),(5,'Carla Ruiz','0993837264','Victor Emilio Estrada'),(6,'Manuel Díaz','0987654321','ESPOL'),(7,'Patricia López','0912345678','Las peñas'),(8,'Diego Herrera','0994736285','km 12.5 via a salitre'),(9,'Laura Rojas','0995748293','Debajo de un puente'),(10,'Andrés Ortega','0994837163','Alborada novena etapa');
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gerenteadm`
--

DROP TABLE IF EXISTS `gerenteadm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gerenteadm` (
  `cedula` int NOT NULL,
  `nomCompleto` varchar(40) NOT NULL,
  PRIMARY KEY (`cedula`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gerenteadm`
--

LOCK TABLES `gerenteadm` WRITE;
/*!40000 ALTER TABLE `gerenteadm` DISABLE KEYS */;
INSERT INTO `gerenteadm` VALUES (991426578,'Estefany Daniela Gonzales Lopez');
/*!40000 ALTER TABLE `gerenteadm` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gerenteventa`
--

DROP TABLE IF EXISTS `gerenteventa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gerenteventa` (
  `cedula` int NOT NULL,
  `nomCompleto` varchar(40) NOT NULL,
  PRIMARY KEY (`cedula`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gerenteventa`
--

LOCK TABLES `gerenteventa` WRITE;
/*!40000 ALTER TABLE `gerenteventa` DISABLE KEYS */;
INSERT INTO `gerenteventa` VALUES (991426578,'Juan Rodolfo Vaquerizo Bravo');
/*!40000 ALTER TABLE `gerenteventa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ordencompra`
--

DROP TABLE IF EXISTS `ordencompra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ordencompra` (
  `idOrden` int NOT NULL,
  `fechaEmision` date NOT NULL,
  `fechaLlegada` date NOT NULL,
  `valorTotal` double NOT NULL,
  `ProveedorId` int NOT NULL,
  `ced_adm` int NOT NULL,
  PRIMARY KEY (`idOrden`),
  KEY `ced_adm` (`ced_adm`),
  KEY `ProveedorId` (`ProveedorId`),
  CONSTRAINT `ordencompra_ibfk_1` FOREIGN KEY (`ced_adm`) REFERENCES `gerenteadm` (`cedula`),
  CONSTRAINT `ordencompra_ibfk_2` FOREIGN KEY (`ProveedorId`) REFERENCES `proveedor` (`idProveedor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordencompra`
--

LOCK TABLES `ordencompra` WRITE;
/*!40000 ALTER TABLE `ordencompra` DISABLE KEYS */;
INSERT INTO `ordencompra` VALUES (1,'2023-01-01','2023-01-10',5000.5,1,991426578),(2,'2023-02-01','2023-02-15',7500,2,991426578),(3,'2023-03-01','2023-03-10',6000.75,3,991426578),(4,'2023-04-01','2023-04-15',8000,4,991426578),(5,'2023-05-01','2023-05-10',9000.25,5,991426578),(6,'2023-06-01','2023-06-15',7000.6,6,991426578),(7,'2023-07-01','2023-07-10',5500.9,7,991426578),(8,'2023-08-01','2023-08-15',6500.3,8,991426578),(9,'2023-09-01','2023-09-10',8000.4,9,991426578),(10,'2023-10-01','2023-10-15',9500.8,10,991426578);
/*!40000 ALTER TABLE `ordencompra` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedido`
--

DROP TABLE IF EXISTS `pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedido` (
  `idPedido` int NOT NULL,
  `fechaEntrega` date NOT NULL,
  `valorTotal` double NOT NULL,
  `clienteID` int NOT NULL,
  `ced_Venta` int NOT NULL,
  PRIMARY KEY (`idPedido`),
  KEY `ced_Venta` (`ced_Venta`),
  KEY `clienteID` (`clienteID`),
  CONSTRAINT `pedido_ibfk_1` FOREIGN KEY (`ced_Venta`) REFERENCES `gerenteventa` (`cedula`),
  CONSTRAINT `pedido_ibfk_2` FOREIGN KEY (`clienteID`) REFERENCES `cliente` (`idCliente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido`
--

LOCK TABLES `pedido` WRITE;
/*!40000 ALTER TABLE `pedido` DISABLE KEYS */;
INSERT INTO `pedido` VALUES (1,'2023-01-20',3000.5,3,991426578),(2,'2023-02-20',4000.75,4,991426578),(3,'2023-03-20',2500,2,991426578),(4,'2023-04-20',3200.8,7,991426578),(5,'2023-05-20',3700.9,6,991426578),(6,'2023-06-20',4200.3,10,991426578),(7,'2023-07-20',3300,9,991426578),(8,'2023-08-20',4600.6,8,991426578),(9,'2023-09-20',4100.4,1,991426578),(10,'2023-10-20',4700.5,1,991426578);
/*!40000 ALTER TABLE `pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto`
--

DROP TABLE IF EXISTS `producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producto` (
  `idProducto` int NOT NULL,
  `nombre` char(50) NOT NULL,
  `descripcion` char(100) NOT NULL,
  `costo` double NOT NULL,
  `precioVenta` double NOT NULL,
  `cantidad` int NOT NULL,
  `idOrdenCompra` int NOT NULL,
  `idPedido` int NOT NULL,
  PRIMARY KEY (`idProducto`),
  KEY `idOrdenCompra` (`idOrdenCompra`),
  KEY `idPedido` (`idPedido`),
  CONSTRAINT `producto_ibfk_1` FOREIGN KEY (`idOrdenCompra`) REFERENCES `ordencompra` (`idOrden`),
  CONSTRAINT `producto_ibfk_2` FOREIGN KEY (`idPedido`) REFERENCES `pedido` (`idPedido`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto`
--

LOCK TABLES `producto` WRITE;
/*!40000 ALTER TABLE `producto` DISABLE KEYS */;
INSERT INTO `producto` VALUES (1,'Producto A','Descripción del producto A',50,75,100,1,1),(2,'Producto B','Descripción del producto B',60,90,200,2,2),(3,'Producto C','Descripción del producto C',70,105,150,3,3),(4,'Producto D','Descripción del producto D',80,120,300,4,4),(5,'Producto E','Descripción del producto E',90,135,400,5,5),(6,'Producto F','Descripción del producto F',100,150,500,6,6),(7,'Producto G','Descripción del producto G',110,165,600,7,7),(8,'Producto H','Descripción del producto H',120,180,700,8,8),(9,'Producto I','Descripción del producto I',130,195,800,9,9),(10,'Producto J','Descripción del producto J',140,210,900,10,10);
/*!40000 ALTER TABLE `producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proveedor`
--

DROP TABLE IF EXISTS `proveedor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proveedor` (
  `idProveedor` int NOT NULL,
  `nombreCompleto` char(50) NOT NULL,
  `telefono` char(20) DEFAULT NULL,
  `dirreccion` char(50) NOT NULL,
  `certificación` char(30) NOT NULL,
  `ced_Venta` int NOT NULL,
  PRIMARY KEY (`idProveedor`),
  KEY `ced_Venta` (`ced_Venta`),
  CONSTRAINT `proveedor_ibfk_1` FOREIGN KEY (`ced_Venta`) REFERENCES `gerenteventa` (`cedula`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedor`
--

LOCK TABLES `proveedor` WRITE;
/*!40000 ALTER TABLE `proveedor` DISABLE KEYS */;
INSERT INTO `proveedor` VALUES (1,'Proveedor A','3216549870','Carrera 8 #9-10','ISO9001',991426578),(2,'Proveedor B','3211234567','Avenida 15 #6-3','ISO14001',991426578),(3,'Proveedor C','3123456789','Calle 25 #5-4','ISO27001',991426578),(4,'Proveedor D','3135678901','Avenida 10 #20-6','ISO9001',991426578),(5,'Proveedor E','3147890123','Carrera 6 #3-2','ISO14001',991426578),(6,'Proveedor F','3158901234','Avenida 13 #5-10','ISO27001',991426578),(7,'Proveedor G','3169012345','Calle 12 #6-8','ISO9001',991426578),(8,'Proveedor H','3170123456','Carrera 4 #10-2','ISO14001',991426578),(9,'Proveedor I','3181234567','Calle 8 #20-15','ISO27001',991426578),(10,'Proveedor J','3192345678','Avenida 14 #5-7','ISO9001',991426578);
/*!40000 ALTER TABLE `proveedor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recordatorio`
--

DROP TABLE IF EXISTS `recordatorio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recordatorio` (
  `idRecordatorio` int NOT NULL,
  `titulo` char(50) NOT NULL,
  `descripcion` char(100) NOT NULL,
  `fechaMax` date NOT NULL,
  `nivelRelevancia` int NOT NULL,
  `SecretariaCedula` int NOT NULL,
  `ced_adm` int NOT NULL,
  PRIMARY KEY (`idRecordatorio`),
  KEY `ced_adm` (`ced_adm`),
  KEY `SecretariaCedula` (`SecretariaCedula`),
  CONSTRAINT `recordatorio_ibfk_1` FOREIGN KEY (`ced_adm`) REFERENCES `gerenteadm` (`cedula`),
  CONSTRAINT `recordatorio_ibfk_2` FOREIGN KEY (`SecretariaCedula`) REFERENCES `secretaria` (`cedula`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recordatorio`
--

LOCK TABLES `recordatorio` WRITE;
/*!40000 ALTER TABLE `recordatorio` DISABLE KEYS */;
INSERT INTO `recordatorio` VALUES (1,'Reunión','Planificar reunión con proveedores','2023-01-15',5,994672938,991426578),(2,'Entrega Reporte','Entregar informe de ventas','2023-02-10',4,994672938,991426578),(3,'Seguimiento Pedido','Revisar estado del pedido del cliente #3','2023-03-05',3,994672938,991426578),(4,'Revisión Presupuesto','Actualizar presupuesto anual','2023-04-01',5,994672938,991426578),(5,'Renovación Contrato','Renovar contrato con Proveedor A','2023-04-20',4,994672938,991426578),(6,'Capacitación','Organizar capacitación para el equipo','2023-05-15',3,994672938,991426578),(7,'Evaluación Desempeño','Planificar evaluaciones de desempeño','2023-06-01',5,994672938,991426578),(8,'Compra Equipos','Solicitar compra de nuevos equipos de oficina','2023-06-20',4,994672938,991426578),(9,'Entrega Factura','Revisar entrega de facturas pendientes','2023-07-05',2,994672938,991426578),(10,'Actualización Software','Actualizar sistema de gestión de inventarios','2023-08-10',5,994672938,991426578);
/*!40000 ALTER TABLE `recordatorio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `secretaria`
--

DROP TABLE IF EXISTS `secretaria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `secretaria` (
  `cedula` int NOT NULL,
  `nomCompleto` varchar(50) NOT NULL,
  PRIMARY KEY (`cedula`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `secretaria`
--

LOCK TABLES `secretaria` WRITE;
/*!40000 ALTER TABLE `secretaria` DISABLE KEYS */;
INSERT INTO `secretaria` VALUES (994672938,'Camila Reyes');
/*!40000 ALTER TABLE `secretaria` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-16 20:43:31
