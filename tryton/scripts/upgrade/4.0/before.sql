-- 5.0 -> 5.2
-- [SQL] Remove error translations:
DELETE FROM "ir_translation" WHERE "type" = 'error';

-- [SQL] Remove src_md5 from ir_translation
ALTER TABLE "ir_translation" DROP CONSTRAINT "ir_translation_translation_md5_uniq";
ALTER TABLE "ir_translation" DROP COLUMN "src_md5";

-- [SQL] Remove old users
DELETE FROM "ir_model_data" WHERE model = 'res.user' AND "fs_id" = 'user_chorus' AND module = 'account_fr_chorus';
DELETE FROM "ir_model_data" WHERE model = 'res.user' AND "fs_id" = 'user_post_clearing_moves' AND module = 'account_payment_clearing';
DELETE FROM "ir_model_data" WHERE model = 'res.user' AND "fs_id" = 'user_stripe' AND module = 'account_payment_stripe';
DELETE FROM "ir_model_data" WHERE model = 'res.user' AND "fs_id" = 'user_marketing_automation' AND module = 'marketing_automation';
DELETE FROM "ir_model_data" WHERE model = 'res.user' AND "fs_id" = 'user_generate_line_consumption' AND module = 'sale_subscription';
DELETE FROM "ir_model_data" WHERE model = 'res.user' AND "fs_id" = 'user_generate_line_consumption' AND module = 'sale_subscription';
DELETE FROM "ir_model_data" WHERE model = 'res.user' AND "fs_id" = 'user_generate_invoice' AND module = 'sale_subscription';
DELETE FROM "ir_model_data" WHERE model = 'res.user' AND "fs_id" = 'user_role' AND module = 'user_role';
DELETE FROM "ir_model_data" WHERE model = 'res.user' AND "fs_id" = 'user_trigger' AND module = 'res';


-- 5.2 -> 5.4
-- [SQL] replace account_payment_sepa_message from TEXT to BYTEA:

ALTER TABLE "account_payment_sepa_message" ALTER COLUMN "message" TYPE BYTEA USING message::BYTEA;

-- 5.4 -> 5.6
-- [SQL] update project status based on previous state
UPDATE project_work SET status = db_id FROM ir_model_data WHERE module = 'project' AND fs_id = 'work_open_status' AND state = 'opened';
UPDATE project_work SET status = db_id FROM ir_model_data WHERE module = 'project' and fs_id

-- [SQL] before update, the foreign key of shipment_party of sale amendment must be recreated
ALTER TABLE sale_amendment_line DROP CONSTRAINT sale_amendment_line_shipment_party_fkey;


-- 5.8 -> 6.0
-- [SQL] fix currency, invoice_type and party on invoice line
UPDATE account_invoice_line SET currency = (SELECT currency FROM account_invoice WHERE id = account_invoice_line.invoice);
UPDATE account_invoice_line SET invoice_type = (SELECT type FROM account_invoice WHERE id = account_invoice_line.invoice) WHERE invoice_type IS NOT NULL;
UPDATE account_invoice_line SET party = (SELECT party FROM account_invoice WHERE id = account_invoice_line.invoice) WHERE party IS NOT NULL;

-- [SQL] before update, add access on field
ALTER TABLE ir_model_field ADD COLUMN "access" BOOLEAN

