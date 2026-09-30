SELECT*
FROM user
JOIN post
ON user.user_id = post.user_id
WHERE user.user_postal_code = 98128;