#include <initializer_list>
#include <utility>

namespace folly
{
    inline constexpr std::size_t sum()
    {
        return 0;
    }

    template <typename... Args>
    inline constexpr std::size_t sum(std::size_t v1, Args... vs)
    {
        return v1 + sum(vs...);
    }
}

namespace initializer_list
{
    inline constexpr std::size_t sum()
    {
        return 0;
    }

    template <typename... Args>
    inline constexpr std::size_t sum(std::size_t v1, Args... vs)
    {
        return ((void)std::initializer_list<std::size_t>{ (v1 += vs)...}, v1);
    }
}

namespace details
{
    template <std::size_t... Is>
    constexpr auto call_sum_impl(std::index_sequence<Is...>)
    {
        return NAMESPACE::sum(Is...);
    }
}

template <std::size_t NumberOfElements>
constexpr auto call_sum()
{
    return details::call_sum_impl(std::make_index_sequence<NumberOfElements>{});
}

int main()
{
    return call_sum<NUMBER_OF_ELEMENTS>();
}