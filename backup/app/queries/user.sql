-- key: user.create
-- INSERT INTO USERS (USER_ID, USER_NAME)
-- VALUES (:user_id, :user_name)

-- key: user.get_user_by_id
SELECT GROUP_SQ, SITE_SQ, USER_SQ, ROLL_CD, USER_NM, USER_ID
FROM TB_M1_INFO_USER_BASE
WHERE USER_ID = :user_id