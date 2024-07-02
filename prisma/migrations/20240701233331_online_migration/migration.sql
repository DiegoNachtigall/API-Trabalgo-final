-- CreateEnum
CREATE TYPE "Generos" AS ENUM ('Acao', 'Puzzle', 'Aventura', 'RPG', 'Estrategia', 'Simulacao', 'FPS', 'RougueLike', 'Plataforma', 'MMO');

-- CreateTable
CREATE TABLE "jogos" (
    "id" SERIAL NOT NULL,
    "nome" VARCHAR(60) NOT NULL,
    "descricao" VARCHAR(40) NOT NULL,
    "preco" DOUBLE PRECISION NOT NULL,
    "genero" "Generos" NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,
    "usuarioId" INTEGER NOT NULL,
    "deleted" BOOLEAN NOT NULL DEFAULT false,

    CONSTRAINT "jogos_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "usuarios" (
    "id" SERIAL NOT NULL,
    "nome" VARCHAR(60) NOT NULL,
    "email" VARCHAR(40) NOT NULL,
    "senha" VARCHAR(60) NOT NULL,
    "deleted" BOOLEAN NOT NULL DEFAULT false,
    "tentativasLogin" INTEGER NOT NULL DEFAULT 0,
    "blocked" BOOLEAN NOT NULL DEFAULT false,

    CONSTRAINT "usuarios_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "logs" (
    "id" SERIAL NOT NULL,
    "descricao" VARCHAR(60) NOT NULL,
    "complemento" VARCHAR(40) NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,
    "usuarioId" INTEGER NOT NULL,

    CONSTRAINT "logs_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "logs" ADD CONSTRAINT "logs_usuarioId_fkey" FOREIGN KEY ("usuarioId") REFERENCES "usuarios"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
