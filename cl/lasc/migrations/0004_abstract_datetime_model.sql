BEGIN;
--
-- Alter field date_created on action
--
ALTER TABLE "lasc_action" ALTER COLUMN "date_created" SET DEFAULT '2020-12-23T15:02:30.093150+00:00'::timestamptz;
ALTER TABLE "lasc_action" ALTER COLUMN "date_created" DROP DEFAULT;
--
-- Alter field date_modified on action
--
ALTER TABLE "lasc_action" ALTER COLUMN "date_modified" SET DEFAULT '2020-12-23T15:02:30.106215+00:00'::timestamptz;
ALTER TABLE "lasc_action" ALTER COLUMN "date_modified" DROP DEFAULT;
--
-- Alter field date_created on crossreference
--
ALTER TABLE "lasc_crossreference" ALTER COLUMN "date_created" SET DEFAULT '2020-12-23T15:02:30.181428+00:00'::timestamptz;
ALTER TABLE "lasc_crossreference" ALTER COLUMN "date_created" DROP DEFAULT;
--
-- Alter field date_modified on crossreference
--
ALTER TABLE "lasc_crossreference" ALTER COLUMN "date_modified" SET DEFAULT '2020-12-23T15:02:30.192444+00:00'::timestamptz;
ALTER TABLE "lasc_crossreference" ALTER COLUMN "date_modified" DROP DEFAULT;
--
-- Alter field date_created on docket
--
ALTER TABLE "lasc_docket" ALTER COLUMN "date_created" SET DEFAULT '2020-12-23T15:02:30.204412+00:00'::timestamptz;
ALTER TABLE "lasc_docket" ALTER COLUMN "date_created" DROP DEFAULT;
--
-- Alter field date_modified on docket
--
ALTER TABLE "lasc_docket" ALTER COLUMN "date_modified" SET DEFAULT '2020-12-23T15:02:30.216012+00:00'::timestamptz;
ALTER TABLE "lasc_docket" ALTER COLUMN "date_modified" DROP DEFAULT;
--
-- Alter field date_created on documentfiled
--
ALTER TABLE "lasc_documentfiled" ALTER COLUMN "date_created" SET DEFAULT '2020-12-23T15:02:30.231283+00:00'::timestamptz;
ALTER TABLE "lasc_documentfiled" ALTER COLUMN "date_created" DROP DEFAULT;
--
-- Alter field date_modified on documentfiled
--
ALTER TABLE "lasc_documentfiled" ALTER COLUMN "date_modified" SET DEFAULT '2020-12-23T15:02:30.243361+00:00'::timestamptz;
ALTER TABLE "lasc_documentfiled" ALTER COLUMN "date_modified" DROP DEFAULT;
--
-- Alter field date_created on documentimage
--
ALTER TABLE "lasc_documentimage" ALTER COLUMN "date_created" SET DEFAULT '2020-12-23T15:02:30.256100+00:00'::timestamptz;
ALTER TABLE "lasc_documentimage" ALTER COLUMN "date_created" DROP DEFAULT;
--
-- Alter field date_modified on documentimage
--
ALTER TABLE "lasc_documentimage" ALTER COLUMN "date_modified" SET DEFAULT '2020-12-23T15:02:30.268436+00:00'::timestamptz;
ALTER TABLE "lasc_documentimage" ALTER COLUMN "date_modified" DROP DEFAULT;
--
-- Alter field date_created on lascjson
--
ALTER TABLE "lasc_lascjson" ALTER COLUMN "date_created" SET DEFAULT '2020-12-23T15:02:30.275797+00:00'::timestamptz;
ALTER TABLE "lasc_lascjson" ALTER COLUMN "date_created" DROP DEFAULT;
--
-- Alter field date_modified on lascjson
--
ALTER TABLE "lasc_lascjson" ALTER COLUMN "date_modified" SET DEFAULT '2020-12-23T15:02:30.281384+00:00'::timestamptz;
ALTER TABLE "lasc_lascjson" ALTER COLUMN "date_modified" DROP DEFAULT;
--
-- Alter field date_created on lascpdf
--
ALTER TABLE "lasc_lascpdf" ALTER COLUMN "date_created" SET DEFAULT '2020-12-23T15:02:30.287007+00:00'::timestamptz;
ALTER TABLE "lasc_lascpdf" ALTER COLUMN "date_created" DROP DEFAULT;
--
-- Alter field date_modified on lascpdf
--
ALTER TABLE "lasc_lascpdf" ALTER COLUMN "date_modified" SET DEFAULT '2020-12-23T15:02:30.295727+00:00'::timestamptz;
ALTER TABLE "lasc_lascpdf" ALTER COLUMN "date_modified" DROP DEFAULT;
--
-- Alter field date_created on party
--
ALTER TABLE "lasc_party" ALTER COLUMN "date_created" SET DEFAULT '2020-12-23T15:02:30.312767+00:00'::timestamptz;
ALTER TABLE "lasc_party" ALTER COLUMN "date_created" DROP DEFAULT;
--
-- Alter field date_modified on party
--
ALTER TABLE "lasc_party" ALTER COLUMN "date_modified" SET DEFAULT '2020-12-23T15:02:30.326633+00:00'::timestamptz;
ALTER TABLE "lasc_party" ALTER COLUMN "date_modified" DROP DEFAULT;
--
-- Alter field date_created on proceeding
--
ALTER TABLE "lasc_proceeding" ALTER COLUMN "date_created" SET DEFAULT '2020-12-23T15:02:30.339902+00:00'::timestamptz;
ALTER TABLE "lasc_proceeding" ALTER COLUMN "date_created" DROP DEFAULT;
--
-- Alter field date_modified on proceeding
--
ALTER TABLE "lasc_proceeding" ALTER COLUMN "date_modified" SET DEFAULT '2020-12-23T15:02:30.352901+00:00'::timestamptz;
ALTER TABLE "lasc_proceeding" ALTER COLUMN "date_modified" DROP DEFAULT;
--
-- Alter field date_created on queuedcase
--
ALTER TABLE "lasc_queuedcase" ALTER COLUMN "date_created" SET DEFAULT '2020-12-23T15:02:30.359017+00:00'::timestamptz;
ALTER TABLE "lasc_queuedcase" ALTER COLUMN "date_created" DROP DEFAULT;
--
-- Alter field date_modified on queuedcase
--
ALTER TABLE "lasc_queuedcase" ALTER COLUMN "date_modified" SET DEFAULT '2020-12-23T15:02:30.363768+00:00'::timestamptz;
ALTER TABLE "lasc_queuedcase" ALTER COLUMN "date_modified" DROP DEFAULT;
--
-- Alter field date_created on queuedpdf
--
ALTER TABLE "lasc_queuedpdf" ALTER COLUMN "date_created" SET DEFAULT '2020-12-23T15:02:30.381910+00:00'::timestamptz;
ALTER TABLE "lasc_queuedpdf" ALTER COLUMN "date_created" DROP DEFAULT;
--
-- Alter field date_modified on queuedpdf
--
ALTER TABLE "lasc_queuedpdf" ALTER COLUMN "date_modified" SET DEFAULT '2020-12-23T15:02:30.397873+00:00'::timestamptz;
ALTER TABLE "lasc_queuedpdf" ALTER COLUMN "date_modified" DROP DEFAULT;
--
-- Alter field date_created on tentativeruling
--
ALTER TABLE "lasc_tentativeruling" ALTER COLUMN "date_created" SET DEFAULT '2020-12-23T15:02:30.411282+00:00'::timestamptz;
ALTER TABLE "lasc_tentativeruling" ALTER COLUMN "date_created" DROP DEFAULT;
--
-- Alter field date_modified on tentativeruling
--
ALTER TABLE "lasc_tentativeruling" ALTER COLUMN "date_modified" SET DEFAULT '2020-12-23T15:02:30.424213+00:00'::timestamptz;
ALTER TABLE "lasc_tentativeruling" ALTER COLUMN "date_modified" DROP DEFAULT;
COMMIT;
