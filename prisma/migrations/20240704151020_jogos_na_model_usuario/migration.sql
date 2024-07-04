-- AlterTable
ALTER TABLE "jogos" ALTER COLUMN "createdAt" SET DATA TYPE TIMESTAMPTZ(3);

-- AddForeignKey
ALTER TABLE "jogos" ADD CONSTRAINT "jogos_usuarioId_fkey" FOREIGN KEY ("usuarioId") REFERENCES "usuarios"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
