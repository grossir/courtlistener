BEGIN;
--
-- Alter field date_created on audio
--
ALTER TABLE "audio_audio" ALTER COLUMN "date_created" SET DEFAULT '2020-12-23T15:00:33.928299+00:00'::timestamptz;
ALTER TABLE "audio_audio" ALTER COLUMN "date_created" DROP DEFAULT;
COMMIT;
