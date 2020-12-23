BEGIN;
--
-- Alter field date_created on donation
--
ALTER TABLE "donate_donation" ALTER COLUMN "date_created" SET DEFAULT '2020-12-23T15:01:16.073701+00:00'::timestamptz;
ALTER TABLE "donate_donation" ALTER COLUMN "date_created" DROP DEFAULT;
--
-- Alter field date_modified on donation
--
ALTER TABLE "donate_donation" ALTER COLUMN "date_modified" SET DEFAULT '2020-12-23T15:01:16.085370+00:00'::timestamptz;
ALTER TABLE "donate_donation" ALTER COLUMN "date_modified" DROP DEFAULT;
--
-- Alter field date_created on monthlydonation
--
ALTER TABLE "donate_monthlydonation" ALTER COLUMN "date_created" SET DEFAULT '2020-12-23T15:01:16.095952+00:00'::timestamptz;
ALTER TABLE "donate_monthlydonation" ALTER COLUMN "date_created" DROP DEFAULT;
--
-- Alter field date_modified on monthlydonation
--
ALTER TABLE "donate_monthlydonation" ALTER COLUMN "date_modified" SET DEFAULT '2020-12-23T15:01:16.194187+00:00'::timestamptz;
ALTER TABLE "donate_monthlydonation" ALTER COLUMN "date_modified" DROP DEFAULT;
COMMIT;
