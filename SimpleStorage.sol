// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract SimpleStorage {

    // this would initialize to zero
    uint256 favorite_number; 
    bool favorite_bool = true;

    struct People {
    uint256 favorite_number;
    string name;
    }

    People[] public people;
    mapping(string => uint256) public name_to_favorite_number;

    function store(uint256 num) public {
        favorite_number = num;
    }

    function retrieve() public view returns (uint256) {
        return favorite_number;
    }

    function add_person(string memory name, uint256 number) public{
        people.push(People({name: name, favorite_number: number}));
        name_to_favorite_number[name] = number;
    }

}