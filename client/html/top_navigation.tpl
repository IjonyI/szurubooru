<nav id='top-navigation' class='buttons'><!--
    --><ul><!--
        --><% for (let item of ctx.items) { %><!--
            --><% if (item.available) { %><!--
                --><li data-name='<%- item.key %>'><!--
                    --><a href='<%- item.url %>' accesskey='<%- item.accessKey %>'><!--
                        --><% if (item.imageUrl) { print(ctx.makeThumbnail(item.imageUrl)); } %><!--
                        --><span class='text'><%= ctx.makeAccessKey(item.title, item.accessKey) %></span><!--
                    --></a><!--
                --></li><!--
            --><% } %><!--
        --><% } %><!--
    --></ul><!--
--></nav>
