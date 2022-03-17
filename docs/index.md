# weiboAPI

搜集微博 API，详情请见下面的示例。

<script src='https://cdn.jsdelivr.net/gh/upupming/weiboAPI@a5de545b607837d4c2793eb6e6e085ea9d361807/response.js'></script>

## userInfo

`https://m.weibo.cn/api/container/getIndex?type=uid&value=1669879400`

<div id="userInfo"></div>
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/renderjson@1.4.0/renderjson.js"></script>
<script>
    renderjson.set_show_to_level(2);
    document.getElementById("userInfo").appendChild(
        renderjson(userInfo)
    );
</script>

## cards

`https://m.weibo.cn/api/container/getIndex?type=uid&value=1669879400&containerid=1076031669879400`

<div id="cards1"></div>
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/renderjson@1.4.0/renderjson.js"></script>
<script>
    renderjson.set_show_to_level(2);
    document.getElementById("cards1").appendChild(
        renderjson(cards1)
    );
</script>

## statuses

`https://m.weibo.cn/statuses/extend?id=4383487819465288`

<div id="status1dd"></div>
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/renderjson@1.4.0/renderjson.js"></script>
<script>
    renderjson.set_show_to_level(2);
    document.getElementById("status1dd").appendChild(
        renderjson(statuses1)
    );
</script>

## retweet

`https://m.weibo.cn/statuses/show?id=HyZVegYAP`

<div id="retweet01"></div>
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/renderjson@1.4.0/renderjson.js"></script>
<script>
    renderjson.set_show_to_level(2);
    document.getElementById("retweet01").appendChild(
        renderjson(retweet01)
    );
</script>

## comments1

`https://m.weibo.cn/api/comments/show?id=4383183661430868&page=1`

<div id="comments1dd"></div>
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/renderjson@1.4.0/renderjson.js"></script>
<script>
    renderjson.set_show_to_level(2);
    document.getElementById("comments1dd").appendChild(
        renderjson(comments1)
    );
</script>

## comments2

`https://m.weibo.cn/comments/hotflow?id=4383183661430868&mid=4383183661430868&max_id_type=0`

<div id="comments2dd"></div>

<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/renderjson@1.4.0/renderjson.js"></script>
<script>
    renderjson.set_show_to_level(2);
    document.getElementById("comments2dd").appendChild(
        renderjson(comments2)
    );
</script>

